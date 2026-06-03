# Open Data Lakehouse - Ingestion

Data ingestion repository containing source connectors, ingestion jobs, validation logic and writers for local and cloud-like storage targets.

## Overview

This repository is responsible for the ingestion layer of the Open Data Lakehouse Lab. It handles fetching data from various public sources and persisting it to landing zones.

### M1 - Weather Ingestion MVP

The current scope is focusing on the Weather Ingestion MVP.
Selected MVP dataset: `meteocat-weather`.

**Note:** The current implementation uses placeholder sample extraction. Real API ingestion will be implemented in future phases.

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

Options for real mode:
- `--mode`: `sample` (default) or `real`.
- `--meteocat-resource`: `stations-metadata` (default).
- `--station-status`: Filter by station status (default: `all`).
- `--metadata-date`: Filter by metadata date (YYYY-MM-DD).

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
