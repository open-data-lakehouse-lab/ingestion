import pytest
import respx
import httpx
from typer.testing import CliRunner
from odl_ingestion.cli import app
from odl_ingestion.connectors.weather.meteocat import MeteocatConnector

runner = CliRunner()

@pytest.fixture
def mock_catalog(tmp_path):
    catalog_path = tmp_path / "catalog"
    dataset_dir = catalog_path / "datasets" / "meteocat-weather"
    dataset_dir.mkdir(parents=True)
    dataset_yml = dataset_dir / "dataset.yml"
    dataset_yml.write_text("""
id: meteocat-weather
name: Meteocat Weather
status: selected
category: weather
format: json
""")
    return catalog_path

def test_ingest_sample_mode(mock_catalog, tmp_path):
    output_dir = tmp_path / "output"
    result = runner.invoke(app, [
        "ingest",
        "--dataset", "meteocat-weather",
        "--catalog-path", str(mock_catalog),
        "--output-dir", str(output_dir),
        "--mode", "sample"
    ])
    assert result.exit_code == 0
    assert "Extracting sample from meteocat-weather" in result.output
    assert (output_dir / "landing" / "weather" / "meteocat" / "meteocat-weather").exists()
    # Check if sample.json is created
    assert any((output_dir / "landing").rglob("sample.json"))

def test_ingest_real_mode_missing_api_key(mock_catalog, tmp_path, monkeypatch):
    monkeypatch.delenv("METEOCAT_API_KEY", raising=False)
    output_dir = tmp_path / "output"
    result = runner.invoke(app, [
        "ingest",
        "--dataset", "meteocat-weather",
        "--catalog-path", str(mock_catalog),
        "--output-dir", str(output_dir),
        "--mode", "real"
    ])
    assert result.exit_code == 1
    assert "Error: METEOCAT_API_KEY environment variable is required for real mode." in result.output

@respx.mock
def test_ingest_real_mode_success(mock_catalog, tmp_path, monkeypatch):
    monkeypatch.setenv("METEOCAT_API_KEY", "test-api-key")
    output_dir = tmp_path / "output"
    
    # Mock Meteocat API
    respx.get("https://api.meteo.cat/xema/v1/estacions/metadades").mock(
        return_value=httpx.Response(200, json={"stations": []})
    )
    
    result = runner.invoke(app, [
        "ingest",
        "--dataset", "meteocat-weather",
        "--catalog-path", str(mock_catalog),
        "--output-dir", str(output_dir),
        "--mode", "real",
        "--meteocat-resource", "stations-metadata"
    ])
    
    assert result.exit_code == 0
    assert "Extracting stations-metadata from meteocat-weather (real mode)..." in result.output
    assert any((output_dir / "landing").rglob("stations-metadata.json"))

def test_connector_extract_station_metadata_params(monkeypatch):
    connector = MeteocatConnector()
    
    with respx.mock:
        mock_route = respx.get("https://api.meteo.cat/xema/v1/estacions/metadades").mock(
            return_value=httpx.Response(200, json={"ok": True})
        )
        
        connector.extract_station_metadata(api_key="key", station_status="active", metadata_date="2024-01-01")
        
        assert mock_route.called
        params = mock_route.calls.last.request.url.params
        assert params["estat"] == "active"
        assert params["data"] == "2024-01-01"
        assert mock_route.calls.last.request.headers["x-api-key"] == "key"

def test_connector_extract_station_metadata_no_params(monkeypatch):
    connector = MeteocatConnector()
    
    with respx.mock:
        mock_route = respx.get("https://api.meteo.cat/xema/v1/estacions/metadades").mock(
            return_value=httpx.Response(200, json={"ok": True})
        )
        
        connector.extract_station_metadata(api_key="key", station_status="all", metadata_date=None)
        
        assert mock_route.called
        params = mock_route.calls.last.request.url.params
        assert "estat" not in params
        assert "data" not in params
        assert mock_route.calls.last.request.headers["x-api-key"] == "key"

def test_ingest_real_mode_measured_variable_missing_args(mock_catalog, tmp_path, monkeypatch):
    monkeypatch.setenv("METEOCAT_API_KEY", "test-api-key")
    output_dir = tmp_path / "output"
    result = runner.invoke(app, [
        "ingest",
        "--dataset", "meteocat-weather",
        "--catalog-path", str(mock_catalog),
        "--output-dir", str(output_dir),
        "--mode", "real",
        "--meteocat-resource", "measured-variable",
        "--variable-code", "32"
        # Missing year, month, day
    ])
    assert result.exit_code == 1
    assert "Error: --variable-code, --year, --month and --day are required for measured-variable resource." in result.output

@respx.mock
def test_ingest_real_mode_measured_variable_success(mock_catalog, tmp_path, monkeypatch):
    monkeypatch.setenv("METEOCAT_API_KEY", "test-api-key")
    output_dir = tmp_path / "output"
    
    # Mock Meteocat API
    respx.get("https://api.meteo.cat/xema/v1/variables/mesurades/32/2026/6/3").mock(
        return_value=httpx.Response(200, json={"data": []})
    )
    
    result = runner.invoke(app, [
        "ingest",
        "--dataset", "meteocat-weather",
        "--catalog-path", str(mock_catalog),
        "--output-dir", str(output_dir),
        "--mode", "real",
        "--meteocat-resource", "measured-variable",
        "--variable-code", "32",
        "--year", "2026",
        "--month", "6",
        "--day", "3"
    ])
    
    assert result.exit_code == 0
    assert "Extracting measured-variable from meteocat-weather (real mode)..." in result.output
    assert any((output_dir / "landing").rglob("measured-variable.json"))

def test_connector_extract_measured_variable_endpoint_and_headers():
    connector = MeteocatConnector()
    
    with respx.mock:
        mock_route = respx.get("https://api.meteo.cat/xema/v1/variables/mesurades/32/2026/6/3").mock(
            return_value=httpx.Response(200, json={"ok": True})
        )
        
        connector.extract_measured_variable(
            api_key="test-key",
            variable_code="32",
            year=2026,
            month=6,
            day=3
        )
        
        assert mock_route.called
        assert mock_route.calls.last.request.headers["x-api-key"] == "test-key"
        assert "codiEstacio" not in mock_route.calls.last.request.url.params

def test_connector_extract_measured_variable_with_station():
    connector = MeteocatConnector()
    
    with respx.mock:
        mock_route = respx.get("https://api.meteo.cat/xema/v1/variables/mesurades/32/2026/6/3").mock(
            return_value=httpx.Response(200, json={"ok": True})
        )
        
        connector.extract_measured_variable(
            api_key="test-key",
            variable_code="32",
            year=2026,
            month=6,
            day=3,
            station_code="D5"
        )
        
        assert mock_route.called
        assert mock_route.calls.last.request.url.params["codiEstacio"] == "D5"
