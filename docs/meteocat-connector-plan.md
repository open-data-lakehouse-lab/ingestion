# Meteocat Connector Plan

## Status: Skeleton

The Meteocat connector is currently in a skeleton state. It provides a placeholder `extract_sample()` method that returns static data for testing the ingestion flow.

## Implementation Steps

1. **Endpoint Selection**: Identify the most relevant Meteocat API endpoints for the MVP (e.g., current weather observations).
2. **Authentication**: Implement secure API key handling using the `METEOCAT_API_KEY` environment variable.
3. **Extraction Logic**: Use `httpx` to perform real API requests.
4. **Partitioning**: Implement date-based partitioning if the API supports it.
5. **Error Handling**: Add robust handling for rate limits, network timeouts, and API errors.
6. **Schema Mapping**: Map Meteocat API responses to a standardized internal format.

## Verification

Before moving to production, real API behavior must be validated against expected schemas and data quality standards.
