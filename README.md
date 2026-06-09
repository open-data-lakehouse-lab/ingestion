# Open Data Lakehouse - Ingestion

Data ingestion repository containing source connectors, ingestion jobs, validation logic and writers for local and cloud-like storage targets.

## Overview

This repository is responsible for the ingestion layer of the Open Data Lakehouse Lab. It handles fetching data from various public sources and persisting it to landing zones.

### M1 - Weather Ingestion MVP

The current scope is focusing on the Weather Ingestion MVP.
Selected MVP dataset: `meteocat-weather`.

**Note:** The default implementation uses safe placeholder sample extraction. Real Meteocat ingestion is available as an explicit opt-in mode for selected resources and requires METEOCAT_API_KEY.

## Installation

### Development Setup

1. Install development dependencies:
   ```bash
   python3 -m pip install -r requirements-dev.txt
   ```

2. Install the package in editable mode:
   ```bash
   python3 -m pip install -e .
   ```

## Usage

### CLI Commands

Check the version:
```bash
odl-ingestion version
```

List available datasets from the catalog:
```bash
odl-ingestion datasets list --catalog-path ../datasets-catalog
```

Show dataset details:
```bash
odl-ingestion datasets show meteocat-weather --catalog-path ../datasets-catalog
```

### Ingestion

Run sample ingestion (safe, offline, no API key required):
```bash
odl-ingestion ingest \
  --dataset meteocat-weather \
  --catalog-path ../datasets-catalog \
  --target local \
  --output-dir ./data \
  --mode sample
```

Run real ingestion (requires `METEOCAT_API_KEY`):

**Stations Metadata:**
```bash
export METEOCAT_API_KEY="replace-me"
odl-ingestion ingest \
  --dataset meteocat-weather \
  --catalog-path ../datasets-catalog \
  --target local \
  --output-dir ./data \
  --mode real \
  --meteocat-resource stations-metadata
```

**Variables Metadata:**
```bash
export METEOCAT_API_KEY="replace-me"
odl-ingestion ingest \
  --dataset meteocat-weather \
  --catalog-path ../datasets-catalog \
  --target local \
  --output-dir ./data \
  --mode real \
  --meteocat-resource variables-metadata
```

**Measured Variable:**
```bash
export METEOCAT_API_KEY="replace-me"
odl-ingestion ingest \
  --dataset meteocat-weather \
  --catalog-path ../datasets-catalog \
  --target local \
  --output-dir ./data \
  --mode real \
  --meteocat-resource measured-variable \
  --variable-code 32 \
  --year 2026 \
  --month 6 \
  --day 3
```

Options for real mode:
- `--mode`: `sample` (default) or `real`.
- `--meteocat-resource`: `stations-metadata` (default), `variables-metadata` or `measured-variable`.
- For `stations-metadata`:
    - `--station-status`: Filter by station status (default: `all`).
    - `--metadata-date`: Filter by metadata date (YYYY-MM-DD).
- For `variables-metadata`:
    - No additional options required.
- For `measured-variable`:
    - `--variable-code`: Variable code (required).
    - `--year`: Year (required).
    - `--month`: Month (required).
    - `--day`: Day (required).
    - `--station-code`: Station code (optional).

### Real-mode Hardening

The Meteocat connector in `real` mode includes hardening for production-like usage:

- **Configurable Timeout**: Set via `METEOCAT_TIMEOUT_SECONDS` (default: 10.0s).
- **Configurable Retries**: Set via `METEOCAT_MAX_RETRIES` (default: 2).
- **Transient Failure Retries**: Automatically retries on:
    - HTTP 429 (Too Many Requests)
    - HTTP 500, 502, 503, 504 (Server Errors)
    - Connection timeouts
- **Safe Error Handling**: Provides clear messages for HTTP errors and invalid JSON without exposing API keys.
- **Mocked Testing**: All tests use mocked HTTP responses and do not require real network or API keys.

**Note:** The default mode is `sample`. Real mode is opt-in and requires a valid API key.

## Validation and Testing

Run the validation script (includes Ruff, Mypy, and Pytest):
```bash
bash scripts/validate.sh
```

## Documentation

- [Ingestion Design](docs/ingestion-design.md)
- [Configuration](docs/configuration.md)
- [Meteocat Connector Plan](docs/meteocat-connector-plan.md)

## License

Unless otherwise noted:

- Software, scripts, Infrastructure as Code, SQL models, configuration files and executable assets are licensed under the [Apache License 2.0](LICENSE).
- Documentation, diagrams and written content are licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

Original upstream datasets, when referenced, remain governed by their original source licenses and terms.
