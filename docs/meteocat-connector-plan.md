# Meteocat Connector Plan

## Status: Real mode for station metadata and measured data (Opt-in)

The Meteocat connector supports both a safe offline `sample` mode and real opt-in mode for:
- `stations-metadata`
- `measured-variable`

## Implementation Progress

1. **Endpoint Selection**: Identified `stations-metadata` and `measured-variable` endpoints. ✓
2. **Authentication**: Implemented `x-api-key` header using the `METEOCAT_API_KEY` environment variable. ✓
3. **Extraction Logic**: Uses `httpx` to perform real API requests. ✓
4. **Partitioning**:
    - Station metadata supports optional date filtering. ✓
    - Measured variable data supports variable code and date (YYYY/MM/DD). ✓
5. **Error Handling**: Uses `response.raise_for_status()` for clear HTTP errors. ✓
6. **Schema Mapping**: Currently returns raw JSON; future mapping to standardized internal format is planned.

## Verification

Real API behavior depends on Meteocat API access and limits. Tests use mocks and do not require network or real secrets.
