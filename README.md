# SOCDocs

SOCDocs is an open collection of practical security operations documentation,
including incident response playbooks, operational procedures, templates, and
related reference material.

The documents in this repository are generated and maintained with
[Skriv](https://github.com/torin-cyber-group/skriv), a structured
document-generation workflow developed by Torin Cyber Group.

## Purpose

SOCDocs provides reusable security documentation that organisations can review,
adapt, and incorporate into their own security operations programs.

The repository may include:

- incident response playbooks;
- security operations procedures;
- tabletop exercise material;
- escalation guides;
- investigation checklists;
- recovery procedures; and
- security governance templates.

These documents provide a practical starting point. They are not designed to be
adopted without review and customisation.

## Repository structure

Each document is stored as a self-contained bundle.

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

A typical bundle contains:

| File | Purpose |
|---|---|
| `README.md` | Overview, intended use, limitations, and document details |
| `request.md` | Source requirements used to generate the document, where approved for publication |
| `final.md` | Published Markdown document |
| `final.pdf` | Printable version of the published document |
| `metadata.yaml` | Version, generation, validation, workflow, and licence metadata |

Some bundles may omit `request.md` where the source request contains information
that is not appropriate for public release.

## Using the documents

You may:

- read and use the documents as reference material;
- adapt them to your organisation;
- redistribute them;
- translate them;
- incorporate portions into other documentation; and
- use them for internal or commercial purposes.

Before using a document operationally, review and adapt it for:

- your organisational structure;
- technology environment;
- security tooling;
- escalation paths;
- legal and regulatory obligations;
- contractual requirements;
- risk appetite;
- incident classification model;
- communications processes; and
- available personnel and external providers.

Names, roles, systems, timeframes, contact details, and decision authorities should
be verified before a document is approved for use.

## Document status

Each published document includes metadata describing:

- its title;
- document type;
- version;
- generation date;
- validation result;
- source workflow; and
- licence.

Documents generated with Skriv may have one of the following deterministic
validation results:

- `Pass`
- `Pass with warnings`

A validation result confirms that defined structural, traceability, consistency,
and publication checks were completed.

It does not prove that a document is:

- factually complete;
- legally compliant;
- suitable for a particular organisation;
- technically correct for every environment; or
- a replacement for professional review or testing.

Documents that fail the publication validation gate are not intended to be included
in this repository.

## Generated with Skriv

The documents in SOCDocs are generated using
[Skriv](https://github.com/torin-cyber-group/skriv).

Skriv uses an ordered document-generation workflow that can include:

- research;
- evidence normalisation;
- drafting;
- technical review;
- revision;
- editing;
- deterministic final validation; and
- deterministic publication packaging.

The publication process creates a local reviewable bundle. It does not
automatically publish files to this repository.

All bundles should be reviewed for confidential, personal, customer-specific, or
organisation-specific information before publication.

## Contributions

Contributions are welcome.

Useful contributions include:

- corrections;
- clearer wording;
- additional technical detail;
- improved operational steps;
- new document scenarios;
- accessibility improvements;
- references to authoritative public guidance; and
- fixes for formatting or broken links.

When contributing changes:

1. Create a branch or fork.
2. Make the proposed change.
3. Explain the reason for the change.
4. Identify any assumptions.
5. Submit a pull request.

Do not submit:

- confidential information;
- customer information;
- credentials or secrets;
- internal network details;
- personal information;
- proprietary threat intelligence;
- unverified claims presented as fact; or
- content that you do not have permission to redistribute.

Contributors should ensure that their submissions can be distributed under the
repository licence.

## Attribution

When reusing or adapting material from SOCDocs, provide reasonable attribution.

Example:

> Adapted from SOCDocs by Torin Cyber Group Pty Ltd, licensed under CC BY 4.0.
>
> https://github.com/torin-cyber-group/SOCDocs

Where practical:

- link to the original document;
- identify the document version;
- indicate that changes were made; and
- retain the licence notice.

## Licence

Unless otherwise stated within a document bundle, the documentation in this
repository is licensed under the
[Creative Commons Attribution 4.0 International Licence](https://creativecommons.org/licenses/by/4.0/).

SPDX identifier: `CC-BY-4.0`

You may share and adapt the material for any purpose, including commercial
purposes, provided that appropriate attribution is given and changes are indicated.
See [LICENSE](LICENSE) for the full legal text.

Copyright © 2026 Torin Cyber Group Pty Ltd.

## Disclaimer

The material in SOCDocs is provided for general informational and operational
reference purposes.

It is not legal advice, regulatory advice, or a guarantee of security. Security
documentation must be adapted to the organisation that will use it and should be
reviewed by appropriately qualified personnel.

Torin Cyber Group Pty Ltd makes no representation that a document is complete,
current, suitable for a particular purpose, or sufficient to meet any legal,
regulatory, contractual, insurance, or compliance obligation.

Operational procedures should be tested through exercises and reviewed after
relevant incidents, organisational changes, technology changes, and changes to
applicable obligations.

## Maintainer

SOCDocs is maintained by Torin Cyber Group Pty Ltd.

Generated documentation tooling: [Skriv](https://github.com/torin-cyber-group/skriv)
