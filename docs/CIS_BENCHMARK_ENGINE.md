# CIS Benchmark Engine

## Purpose

The benchmark engine exists to convert external benchmark source material into project-owned structured data.

That means:

- the app can reason over controls as data
- reports can reference exact benchmark controls
- profiles can be generated from approved controls
- script candidates can be generated from extracted remediation content
- the runtime does not have to depend on the original PDF after extraction

## Current Sources

The engine currently supports:

- structured XML-style sources such as `XCCDF` and related machine-readable formats
- JSON imports
- plain text
- CIS PDF text extraction

For this repo, the important imported sources were:

- Windows 11 CIS benchmark PDF
- Ubuntu 24.04 CIS benchmark PDF

## Where The Code Lives

- [benchmark.py](/E:/T/hardsecnet/hardsecnet-pyside/src/hardsecnet_pyside/benchmark.py)
- [services.py](/E:/T/hardsecnet/hardsecnet-pyside/src/hardsecnet_pyside/services.py)
- [models.py](/E:/T/hardsecnet/hardsecnet-pyside/src/hardsecnet_pyside/models.py)

## Normalized Objects

The importer builds:

- `BenchmarkDocument`
- `BenchmarkItem`
- `CheckLogic`
- `RemediationStep`
- `EvidenceField`

Each imported control is meant to become a structured object with:

- benchmark ID
- title
- OS family
- profile level
- automation hint
- rationale
- recommendation
- audit logic
- remediation guidance
- evidence fields
- source page
- citations
- confidence
- candidate modules

## CIS PDF Parsing Strategy

The parser does not just scan the table of contents.

It tries to detect the actual control bodies and extract sections like:

- `Profile Applicability`
- `Description`
- `Rationale`
- `Impact`
- `Audit`
- `Remediation`
- `Default Value`

That is what turns the PDF from a passive document into usable structured data.

## Durable Export

After import, each benchmark is exported into a durable project-owned bundle under:

- [benchmark_exports](/E:/T/hardsecnet/hardsecnet-pyside/src/hardsecnet_pyside/data/benchmark_exports)

Each bundle contains:

- `benchmark_document.json`
- `benchmark_items.json`
- `scripts/`
- `README.md`

This is the key point:

The system is no longer dependent on the original PDF at runtime for these exported benchmark sets.

## Current Imported Bundles

### Windows 11

- [Windows 11 CIS Bundle](/E:/T/hardsecnet/hardsecnet-pyside/src/hardsecnet_pyside/data/benchmark_exports/cis-microsoft-windows-11-stand-alone-benchmark-v4.0.0)

Current extraction result:

- `477` controls
- `477` generated PowerShell candidate files

### Ubuntu 24.04

- [Ubuntu 24.04 CIS Bundle](/E:/T/hardsecnet/hardsecnet-pyside/src/hardsecnet_pyside/data/benchmark_exports/cis-ubuntu-linux-24.04-lts-benchmark-v1.0.0)

Current extraction result:

- `312` controls
- `312` generated Bash candidate files

## Script Generation

Generated scripts are derived from:

- extracted `Audit` sections
- extracted `Remediation` sections
- control metadata

They are stored both:

- in runtime import output
- in durable repo exports

## What The Generated Scripts Are

They are:

- benchmark-derived script candidates
- traceable to a specific benchmark control
- useful as implementation inputs

They are not automatically:

- production-safe remediations
- fully validated hardening modules
- guaranteed rollback-safe operations

This is especially true for Windows.

Windows CIS content often describes policy state in GPO or registry language, which means the extraction result is often a structured template that still needs engineering.

Ubuntu extracts more naturally because the benchmark text often contains command-shaped remediation content.

## What A New Contributor Should Do Next

If you want to improve the benchmark engine, these are the highest-value tasks:

1. validate and upgrade the generated Ubuntu shell scripts into production-grade modules
2. convert the Windows policy templates into real PowerShell/reg/GPO logic
3. add a UI review workflow for low-confidence controls
4. make exported benchmark bundles load automatically as built-in sources on startup
5. add more tests around wrapped lines, appendix sections, and malformed extraction cases
