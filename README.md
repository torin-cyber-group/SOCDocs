# SOCDocs

<p align="center">

![Documentation](https://img.shields.io/badge/Documentation-Security%20Operations-blue)
![Markdown](https://img.shields.io/badge/Format-Markdown-informational)
![GitHub Actions](https://img.shields.io/github/actions/workflow/status/torin-cyber-group/SOCDocs/build-pdfs.yml?branch=main&label=PDF%20Build)
![Licence](https://img.shields.io/badge/Licence-Community-orange)
![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-brightgreen)

</p>

SOCDocs is an open collection of practical Security Operations Centre (SOC) documentation, including incident response playbooks, operational procedures, templates and supporting reference material.

The documents in this repository are generated and maintained with **Skriv**, a structured document-generation workflow developed by **Torin Cyber Group**.

---

# Table of Contents

- [Purpose](#purpose)
- [Repository Structure](#repository-structure)
- [Automatic PDF Generation](#automatic-pdf-generation)
- [Using the Documents](#using-the-documents)
- [Document Status](#document-status)
- [Generated with Skriv](#generated-with-skriv)
- [Contributions and Feedback](#contributions-and-feedback)
- [Attribution](#attribution)
- [Licensing and Commercial Use](#licensing-and-commercial-use)
- [Disclaimer](#disclaimer)
- [Maintainer](#maintainer)

---

# Purpose

SOCDocs provides reusable security documentation that organisations can review, adapt and incorporate into their own security operations programmes.

The repository includes practical documentation such as:

- Incident response playbooks
- Security operations procedures
- Tabletop exercise material
- Escalation guides
- Investigation checklists
- Recovery procedures
- Security governance templates

These documents are intended as a practical starting point and should always be reviewed, customised and approved before operational use.

---

# Repository Structure

Each document is stored as a self-contained publication bundle.

```text
SOCDocs/
├── README.md
├── LICENSE
├── incident-response/
│   └── ai-data-leakage/
│       ├── README.md
│       ├── request.md
│       ├── final.md
│       ├── final.pdf
│       └── metadata.yaml
├── procedures/
├── tabletop-exercises/
├── templates/
└── other/
```

Typical bundle contents:

| File | Purpose |
|------|----------|
| `README.md` | Overview, intended use, limitations and document details |
| `request.md` | Original generation request (where suitable for publication) |
| `final.md` | Published Markdown document |
| `final.pdf` | Printable PDF generated automatically |
| `metadata.yaml` | Version, validation, workflow and publication metadata |

Some bundles intentionally omit `request.md` where publication could disclose sensitive or unnecessary information.

---

# Automatic PDF Generation

Publication bundles contain reviewed Markdown and metadata.

PDFs are generated automatically after changes are merged into `main`.

The **Build Bundle PDFs** GitHub Actions workflow:

1. Discovers every `final.md`
2. Builds PDFs using MkDocs and `mkdocs-to-pdf`
3. Writes `final.pdf` beside the Markdown source
4. Commits updated PDFs using `github-actions[bot]`

The workflow can also be run manually using **workflow_dispatch**.

---

# Using the Documents

SOCDocs is intended to help organisations accelerate development of their own documentation.

You may use the documents to:

- Learn from existing examples
- Adapt documentation for your organisation
- Translate content
- Incorporate sections into internal documentation
- Build your own operational documentation

Before operational use, every document should be reviewed and customised for your:

- organisational structure
- technology environment
- security tooling
- escalation paths
- legal and regulatory obligations
- contractual requirements
- risk appetite
- incident classification model
- communications processes
- personnel and external providers

Names, contact details, authorities, systems and procedures should always be verified before approval.

---

# Document Status

Each published bundle contains metadata describing:

- Title
- Document type
- Version
- Publication date
- Validation result
- Source workflow
- Licence

Current validation outcomes are:

- `Pass`
- `Pass with warnings`

Validation confirms that publication, consistency and structural checks completed successfully.

It does **not** certify that a document is:

- technically complete
- legally compliant
- suitable for every environment
- a substitute for expert review or testing

---

# Generated with Skriv

SOCDocs is generated using **Skriv**, a structured documentation workflow developed by Torin Cyber Group.

The workflow may include:

- Research
- Evidence normalisation
- Drafting
- Technical review
- Editing
- Deterministic validation
- Publication packaging

Publication bundles are reviewed before being published.

No document should be published without first confirming that confidential, customer-specific or organisation-specific information has been removed.

---

# Contributing
## Contributions and Feedback

Feedback, corrections and improvement suggestions are welcome through GitHub Issues.

Please do not submit pull requests or maintain modified forks for contribution back to this repository. SOCDocs documents are generated and maintained through Skriv, so changes need to be made within the underlying generation workflow rather than applied only to an individual published file.

Useful issues include:

* technical corrections;
* unclear or ambiguous wording;
* missing operational steps;
* inaccurate assumptions;
* formatting or accessibility problems;
* broken links or references;
* suggested document scenarios;
* gaps in existing playbooks or procedures; and
* recommendations for authoritative public guidance.

When opening an issue, include:

1. The affected document and section.
2. A clear description of the issue.
3. The reason a change is needed.
4. Suggested wording or expected behaviour, where practical.
5. Any relevant references or supporting evidence.

Do not include:

* confidential or customer information;
* credentials, secrets or access tokens;
* internal network details;
* personal information;
* proprietary threat intelligence;
* unpublished incident information; or
* material you do not have permission to share.

Accepted improvements will be incorporated into Skriv where appropriate and applied to the relevant generated documents in a future repository update.


---

# Attribution

When adapting SOCDocs, reasonable attribution is appreciated.

Example:

> Adapted from SOCDocs by Torin Cyber Group Pty Ltd.

> https://github.com/torin-cyber-group/SOCDocs

Where practical:

- Link to the original document
- Identify the version used
- State that modifications were made
- Retain licence information

---

# Licensing and Commercial Use

SOCDocs is free to use, modify and adapt **within your own organisation**.

This includes internal use by:

- private organisations
- government agencies
- educational institutions
- not-for-profit organisations

No commercial licence is required for internal operational use.

### Commercial Services

A commercial licence or partnership agreement is required if SOCDocs is used as part of services delivered to third parties.

This includes, but is not limited to:

- Consulting engagements
- Professional advisory services
- Managed Security Services (MSSP)
- Managed Service Providers (MSP)
- Documentation developed for clients
- Security assessments
- Compliance engagements
- Commercial training packages
- Reselling or redistributing SOCDocs as part of a paid offering

If your organisation wishes to use SOCDocs commercially, please contact the maintainer to discuss licensing or partnership options.

Copyright © 2026 Torin Cyber Group Pty Ltd.

---

# Disclaimer

SOCDocs is provided for informational and operational reference purposes only.

The documentation is **not** legal advice, regulatory advice or a guarantee of security.

Every organisation is responsible for reviewing, approving and testing documentation before operational use.

Torin Cyber Group Pty Ltd makes no warranty that any document is complete, current or suitable for a particular environment or compliance obligation.

Operational documentation should be reviewed following security incidents, organisational changes, technology changes and changes to applicable legal or regulatory obligations.

---

# Maintainer

**Torin Cyber Group Pty Ltd**

SOCDocs is maintained by Torin Cyber Group.

For commercial licensing or partnership enquiries, please contact Torin Cyber Group through the GitHub repository or company website.
