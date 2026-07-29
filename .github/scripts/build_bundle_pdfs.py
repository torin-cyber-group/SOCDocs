#!/usr/bin/env python3
"""Build a metadata-named PDF beside every SOCDocs bundle final.md using MkDocs."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
from pathlib import Path
from typing import Any

import yaml

H1_PATTERN = re.compile(r"^# (?!#)(\S.*)$")
MERMAID_FENCE_PATTERN = re.compile(r"^```mermaid[ \t]*$", re.MULTILINE)
FILENAME_SEPARATOR_PATTERN = re.compile(r"[^a-z0-9]+")
FONT_SOURCE_DIRECTORY = Path(__file__).with_name("pdf-assets") / "fonts"
FONT_FILES = {
    "regular": "IBMPlexSans-Regular.woff2",
    "italic": "IBMPlexSans-Italic.woff2",
    "semibold": "IBMPlexSans-SemiBold.woff2",
    "bold": "IBMPlexSans-Bold.woff2",
}


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


def load_metadata(bundle: Path) -> dict[str, Any]:
    """Load and validate metadata used for the cover and output filename."""

    path = bundle / "metadata.yaml"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise PdfBuildError(f"cannot read bundle metadata {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise PdfBuildError(f"bundle metadata must be a mapping: {path}")
    for key in ("title", "document_type", "document_version"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise PdfBuildError(f"{path} must define a non-empty {key}")
    return data


def filename_component(value: str) -> str:
    """Return one portable, lowercase PDF filename component."""

    ascii_value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    component = FILENAME_SEPARATOR_PATTERN.sub("-", ascii_value.casefold()).strip("-")
    if not component:
        raise PdfBuildError(f"cannot derive a filename component from {value!r}")
    return component


def output_filename(metadata: dict[str, Any]) -> str:
    """Build the required type-title-version PDF filename."""

    version = re.sub(
        r"[^a-z0-9.]+",
        "-",
        metadata["document_version"].strip().casefold(),
    ).strip("-.")
    if not version:
        raise PdfBuildError(
            f"cannot derive a filename component from {metadata['document_version']!r}"
        )
    return (
        "-".join(
            (
                filename_component(metadata["document_type"]),
                filename_component(metadata["title"]),
                version,
            )
        )
        + ".pdf"
    )


def metadata_text(metadata: dict[str, Any], *path: str) -> str:
    """Return a nested metadata value as printable text."""

    value: object = metadata
    for key in path:
        if not isinstance(value, dict):
            return ""
        value = value.get(key)
    return str(value) if value is not None else ""


def install_pdf_theme(workspace: Path, docs_dir: Path, metadata: dict[str, Any]) -> Path:
    """Create the monochrome cover template, stylesheet, and local font assets."""

    missing_fonts = [
        filename
        for filename in FONT_FILES.values()
        if not (FONT_SOURCE_DIRECTORY / filename).is_file()
    ]
    if missing_fonts:
        raise PdfBuildError(
            "missing vendored IBM Plex Sans font files: " + ", ".join(missing_fonts)
        )

    font_dir = docs_dir / "assets" / "fonts"
    font_dir.mkdir(parents=True)
    for filename in (*FONT_FILES.values(), "license.txt"):
        shutil.copyfile(FONT_SOURCE_DIRECTORY / filename, font_dir / filename)

    templates = workspace / "templates"
    templates.mkdir()
    (templates / "cover.html").write_text(
        """<article id="doc-cover">
  <div class="cover-kicker">{{ document_type | e }}</div>
  <div class="cover-title">
    <h1>{{ cover_title | e }}</h1>
  </div>
  <dl class="cover-details">
    <dt>Document type</dt><dd>{{ document_type | e }}</dd>
    <dt>Version</dt><dd>{{ document_version | e }}</dd>
    <dt>Status</dt><dd>{{ document_status | e }}</dd>
    <dt>Generated</dt><dd>{{ generated_date | e }}</dd>
    <dt>Validation</dt><dd>{{ validation_result | e }}</dd>
    <dt>Licence</dt><dd>{{ licence | e }}</dd>
  </dl>
  <div class="cover-owner">{{ copyright_holder | e }}</div>
</article>
""",
        encoding="utf-8",
    )
    (templates / "styles.scss").write_text(
        f"""@font-face {{
  font-family: "IBM Plex Sans";
  font-style: normal;
  font-weight: 400;
  src: url("assets/fonts/{FONT_FILES['regular']}") format("woff2");
}}
@font-face {{
  font-family: "IBM Plex Sans";
  font-style: italic;
  font-weight: 400;
  src: url("assets/fonts/{FONT_FILES['italic']}") format("woff2");
}}
@font-face {{
  font-family: "IBM Plex Sans";
  font-style: normal;
  font-weight: 600;
  src: url("assets/fonts/{FONT_FILES['semibold']}") format("woff2");
}}
@font-face {{
  font-family: "IBM Plex Sans";
  font-style: normal;
  font-weight: 700;
  src: url("assets/fonts/{FONT_FILES['bold']}") format("woff2");
}}

@page {{
  background: #fff;
  color: #000;
}}

*, *::before, *::after {{
  border-color: #000 !important;
  color: #000 !important;
  font-family: "IBM Plex Sans", sans-serif !important;
}}

body, article, section, aside, blockquote, code, pre, table, th, td {{
  background: #fff !important;
}}

a {{
  color: #000 !important;
  text-decoration: underline;
}}

h1, h2, h3, h4, h5, h6 {{
  color: #000 !important;
}}

blockquote {{
  border-left: 2px solid #000 !important;
}}

table {{
  border-collapse: collapse;
}}

th, td {{
  border: 1px solid #000 !important;
}}

img[src*="final.rendered-"] {{
  display: block;
  filter: grayscale(100%);
  height: auto;
  margin: 0 auto;
  max-height: 220mm;
  max-width: 100%;
  object-fit: contain;
  width: auto;
}}

article#doc-cover {{
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 18mm 12mm 12mm;
}}

article#doc-cover .cover-kicker {{
  border-bottom: 2px solid #000;
  font-size: 12pt;
  font-weight: 600;
  letter-spacing: 0.08em;
  padding-bottom: 4mm;
  text-transform: uppercase;
}}

article#doc-cover .cover-title {{
  align-items: center;
  display: flex;
  flex: 1 1 auto;
}}

article#doc-cover h1 {{
  font-size: 34pt;
  font-weight: 600;
  line-height: 1.12;
  margin: 0;
}}

article#doc-cover .cover-details {{
  border-top: 1px solid #000;
  display: grid;
  font-size: 10pt;
  grid-template-columns: 38mm 1fr;
  margin: 0;
  padding-top: 5mm;
}}

article#doc-cover .cover-details dt {{
  font-weight: 600;
  margin: 0 0 2mm;
}}

article#doc-cover .cover-details dd {{
  margin: 0 0 2mm;
}}

article#doc-cover .cover-owner {{
  font-size: 9pt;
  margin-top: 8mm;
}}
""",
        encoding="utf-8",
    )
    return templates


def copy_bundle_sources(bundle: Path, docs_dir: Path, output_name: str) -> None:
    """Copy final.md and non-Markdown bundle assets into an isolated docs tree."""

    docs_dir.mkdir(parents=True)
    for source in sorted(bundle.rglob("*")):
        if source.is_symlink():
            raise PdfBuildError(f"bundle content must not be a symbolic link: {source}")
        if not source.is_file():
            continue
        relative = source.relative_to(bundle)
        if source.name in {"final.pdf", output_name}:
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
    puppeteer_config = docs_dir.parent / "puppeteer-config.json"
    mermaid_config = docs_dir.parent / "mermaid-config.json"
    puppeteer_config.write_text(
        json.dumps(
            {
                "args": [
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ]
            }
        ),
        encoding="utf-8",
    )
    mermaid_config.write_text(
        json.dumps(
            {
                "theme": "base",
                "themeVariables": {
                    "background": "#ffffff",
                    "primaryColor": "#ffffff",
                    "primaryTextColor": "#000000",
                    "primaryBorderColor": "#000000",
                    "lineColor": "#000000",
                    "secondaryColor": "#ffffff",
                    "secondaryTextColor": "#000000",
                    "secondaryBorderColor": "#000000",
                    "tertiaryColor": "#ffffff",
                    "tertiaryTextColor": "#000000",
                    "tertiaryBorderColor": "#000000",
                    "noteBkgColor": "#ffffff",
                    "noteTextColor": "#000000",
                    "noteBorderColor": "#000000",
                },
            }
        ),
        encoding="utf-8",
    )
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
            "--puppeteerConfigFile",
            str(puppeteer_config),
            "--configFile",
            str(mermaid_config),
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
    metadata = load_metadata(bundle)
    if metadata["title"] != title:
        raise PdfBuildError(
            f"metadata title does not match the document H1 in {final_document}"
        )
    filename = output_filename(metadata)
    with tempfile.TemporaryDirectory(prefix="socdocs-pdf-") as temporary:
        workspace = Path(temporary)
        docs_dir = workspace / "docs"
        site_dir = workspace / "site"
        config_path = workspace / "mkdocs.yml"
        copy_bundle_sources(bundle, docs_dir, filename)
        render_mermaid_diagrams(docs_dir)
        templates = install_pdf_theme(workspace, docs_dir, metadata)
        config = {
            "site_name": title,
            "site_author": metadata_text(metadata, "copyright_holder"),
            "copyright": metadata_text(metadata, "copyright_holder"),
            "docs_dir": str(docs_dir),
            "site_dir": str(site_dir),
            "use_directory_urls": False,
            "nav": [{"Document": "final.md"}],
            "theme": {"name": "mkdocs"},
            "extra": {
                "document_type": metadata_text(metadata, "document_type"),
                "document_version": metadata_text(metadata, "document_version"),
                "document_status": metadata_text(metadata, "publication", "status"),
                "generated_date": metadata_text(metadata, "generated_date"),
                "validation_result": metadata_text(metadata, "validation", "result"),
                "licence": metadata_text(metadata, "licence", "identifier"),
                "copyright_holder": metadata_text(metadata, "copyright_holder"),
            },
            "plugins": [
                {
                    "to-pdf": {
                        "output_path": filename,
                        "cover": True,
                        "cover_title": title,
                        "custom_template_path": str(templates),
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
        generated = site_dir / filename
        if not generated.is_file() or not generated.read_bytes().startswith(b"%PDF-"):
            raise PdfBuildError(f"MkDocs did not create a valid PDF for {final_document}")
        temporary_pdf = bundle / f".{filename}.tmp"
        try:
            shutil.copyfile(generated, temporary_pdf)
            os.replace(temporary_pdf, bundle / filename)
        finally:
            temporary_pdf.unlink(missing_ok=True)
    legacy_pdf = bundle / "final.pdf"
    if legacy_pdf.exists():
        if legacy_pdf.is_symlink() or not legacy_pdf.is_file():
            raise PdfBuildError(f"legacy PDF must be a regular file: {legacy_pdf}")
        legacy_pdf.unlink()
    print(f"Generated {bundle.relative_to(repository) / filename}")


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
