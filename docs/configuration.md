# Configuration Guide

## Local Configuration

The ingestion tool can be configured via command-line arguments or environment variables.

### Environment Variables

- `CATALOG_PATH`: Path to the dataset catalog repository (default: `../datasets-catalog`).
- `OUTPUT_DIR`: Directory where ingested data will be stored (default: `./data`).
- `METEOCAT_API_KEY`: API key for the Meteocat connector (must NOT be committed). Required only for `real` mode.
- `METEOCAT_BASE_URL`: Base URL for Meteocat API (default: `https://api.meteo.cat/xema/v1`).

## API Keys

Security is a priority. Never commit API keys, tokens, or any other credentials to the repository. Use environment variables or a local `.env` file (which is ignored by git).

## Output Layout

The local writer uses a deterministic layout:

```
<output_dir>/landing/<category>/<source>/<dataset_id>/ingestion_date=YYYY-MM-DD/<filename>.json
```

- For `sample` mode: `sample.json`
- For `stations-metadata` resource: `stations-metadata.json`
- For `variables-metadata` resource: `variables-metadata.json`
- For `measured-variable` resource: `measured-variable.json`
