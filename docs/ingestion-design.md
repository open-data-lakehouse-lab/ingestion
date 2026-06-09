# Ingestion Design

## Overview

The `ingestion` repository is responsible for fetching data from various sources and writing it to different storage targets within the Open Data Lakehouse.

## Responsibilities

- **Source Connectors**: Interface with external APIs and data sources.
- **Writers**: Handle data persistence to local or cloud storage.
- **Catalog Integration**: Use metadata from the dataset catalog to guide ingestion.
- **Validation**: Ensure incoming data meets basic quality and format requirements.

## Architecture

### Connector Abstraction

All connectors inherit from `BaseConnector`, defining a common interface for extraction. This allows the ingestion engine to handle different datasets uniformly.

### Writer Abstraction

Writers inherit from `BaseWriter`, allowing the same data to be written to local files, S3, or other targets by simply switching the writer implementation.

### Local-first Ingestion

To facilitate development and testing, the system supports a local-first ingestion flow where data is written to a local directory structure mimicking a cloud landing zone. It also supports a safe offline `sample` mode as the default behavior.

## Real-world Ingestion

The system supports real-world ingestion through opt-in modes. Implemented real-world resources for Meteocat:
- `stations-metadata`: General information about weather stations.
- `variables-metadata`: Definitions and metadata for all available weather variables.
- `measured-variable`: Values measured by variables (e.g., temperature, humidity) for all stations or a specific station.

Real mode requires a valid `METEOCAT_API_KEY`.

### Meteocat Real-mode Hardening

The Meteocat connector implementation for real mode includes:

- **Configurable timeout and retries** via environment variables.
- **Explicit HTTP status handling** with connector-specific errors.
- **Retry support for transient failures** (HTTP 429, 5xx, and timeouts).
- **Safe error messages** that prevent leaking API keys in logs or CLI output.
- **Invalid JSON handling** to catch unexpected API responses.
- **Mocked HTTP testing** to ensure reliability without requiring network access.

## Future Evolution

- Implementation of cloud-like writers (e.g., S3-compatible storage).
- Advanced schema validation using Pydantic or external schema registries.
- Support for incremental ingestion and partitioning.
