#!/usr/bin/env python3
"""Build final.pdf beside every SOCDocs bundle final.md using MkDocs."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import yaml

H1_PATTERN = re.compile(r"^# (?!#)(\S.*)$")
MERMAID_FENCE_PATTERN = re.compile(r"^```mermaid[ \t]*$", re.MULTILINE)


class PdfBuildError(Exception):
    """An expected bundle discovery or PDF generation failure."""


def discover_final_documents(repository: Path) -> list[Path]:
    """Return every regular, non-symlinked bundle final.md in stable order."""

    documents: list[Path] = []
    for path in repository.rglob("final.md"):
        if ".git" in path.parts:
            continue
        if path.is_symlink() or not path.is_file():
            raise PdfBuildError(f"bundle document must be a regular file: {path}")
        documents.append(path)
    return sorted(documents)


def document_title(path: Path) -> str:
    """Read the required first-line H1 used as the MkDocs site and PDF title."""

    try:
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
    except (OSError, UnicodeError, IndexError) as exc:
        raise PdfBuildError(f"cannot read a title from {path}: {exc}") from exc
    match = H1_PATTERN.fullmatch(first_line)
    if match is None:
        raise PdfBuildError(f"{path} must begin with a non-empty H1 title")
    return match.group(1)


def copy_bundle_sources(bundle: Path, docs_dir: Path) -> None:
    """Copy final.md and non-Markdown bundle assets into an isolated docs tree."""

    docs_dir.mkdir(parents=True)
    for source in sorted(bundle.rglob("*")):
        if source.is_symlink():
            raise PdfBuildError(f"bundle content must not be a symbolic link: {source}")
        if not source.is_file():
            continue
        relative = source.relative_to(bundle)
        if source.name == "final.pdf":
            continue
        if source.suffix.lower() == ".md" and source.name != "final.md":
            continue
        destination = docs_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def render_mermaid_diagrams(docs_dir: Path) -> None:
    """Replace Mermaid fences with print-scaled image references."""

    source = docs_dir / "final.md"
    try:
        markdown = source.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PdfBuildError(f"cannot read copied Markdown {source}: {exc}") from exc
    if MERMAID_FENCE_PATTERN.search(markdown) is None:
        return

    rendered = docs_dir / "final.rendered.md"
    subprocess.run(
        (
            "mmdc",
            "--input",
            source.name,
            "--output",
            rendered.name,
            "--backgroundColor",
            "transparent",
            "--outputFormat",
            "png",
            "--scale",
            "2",
            "--quiet",
        ),
        cwd=docs_dir,
        check=True,
    )
    try:
        rendered_markdown = rendered.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PdfBuildError(f"cannot read Mermaid output {rendered}: {exc}") from exc
    if MERMAID_FENCE_PATTERN.search(rendered_markdown) is not None:
        raise PdfBuildError(f"Mermaid fences remain after rendering {source}")
    if not list(docs_dir.glob("final.rendered-*.png")):
        raise PdfBuildError(f"Mermaid CLI did not create PNG assets for {source}")
    os.replace(rendered, source)


def build_pdf(repository: Path, final_document: Path) -> None:
    """Run MkDocs for one bundle and atomically replace its generated PDF."""

    bundle = final_document.parent
    title = document_title(final_document)
    with tempfile.TemporaryDirectory(prefix="socdocs-pdf-") as temporary:
        workspace = Path(temporary)
        docs_dir = workspace / "docs"
        site_dir = workspace / "site"
        config_path = workspace / "mkdocs.yml"
        copy_bundle_sources(bundle, docs_dir)
        render_mermaid_diagrams(docs_dir)
        (docs_dir / "pdf-render.css").write_text(
            'img[src*="final.rendered-"] {\n'
            "  display: block;\n"
            "  height: auto;\n"
            "  margin: 0 auto;\n"
            "  max-height: 220mm;\n"
            "  max-width: 100%;\n"
            "  object-fit: contain;\n"
            "  width: auto;\n"
            "}\n",
            encoding="utf-8",
        )
        config = {
            "site_name": title,
            "docs_dir": str(docs_dir),
            "site_dir": str(site_dir),
            "use_directory_urls": False,
            "nav": [{"Document": "final.md"}],
            "theme": {"name": "mkdocs"},
            "extra_css": ["pdf-render.css"],
            "plugins": [
                {
                    "to-pdf": {
                        "output_path": "final.pdf",
                        "cover": False,
                        "toc_level": 3,
                    }
                }
            ],
            "markdown_extensions": [
                "admonition",
                "attr_list",
                "fenced_code",
                "tables",
                {"toc": {"permalink": False}},
            ],
        }
        config_path.write_text(
            yaml.safe_dump(config, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        subprocess.run(
            ("mkdocs", "build", "--clean", "--config-file", str(config_path)),
            cwd=repository,
            check=True,
        )
        generated = site_dir / "final.pdf"
        if not generated.is_file() or not generated.read_bytes().startswith(b"%PDF-"):
            raise PdfBuildError(f"MkDocs did not create a valid PDF for {final_document}")
        temporary_pdf = bundle / ".final.pdf.tmp"
        try:
            shutil.copyfile(generated, temporary_pdf)
            os.replace(temporary_pdf, bundle / "final.pdf")
        finally:
            temporary_pdf.unlink(missing_ok=True)
    print(f"Generated {bundle.relative_to(repository) / 'final.pdf'}")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository",
        type=Path,
        default=Path.cwd(),
        help="SOCDocs repository root (default: current directory)",
    )
    return parser.parse_args()


def main() -> int:
    """Build PDFs for all discovered publication bundles."""

    args = parse_args()
    repository = args.repository.resolve()
    if not (repository / ".git").exists():
        raise PdfBuildError(f"not a Git repository: {repository}")
    documents = discover_final_documents(repository)
    if not documents:
        print("No bundle final.md files found; nothing to generate.")
        return 0
    for document in documents:
        build_pdf(repository, document)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (PdfBuildError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"PDF generation failed: {error}") from error
