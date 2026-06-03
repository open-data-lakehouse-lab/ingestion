from typer.testing import CliRunner
from odl_ingestion.cli import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "odl-ingestion version" in result.output

def test_datasets_list_empty(tmp_path):
    catalog_path = tmp_path / "empty_catalog"
    catalog_path.mkdir()
    result = runner.invoke(app, ["datasets", "list", "--catalog-path", str(catalog_path)])
    assert result.exit_code == 0
    assert "No datasets found in catalog" in result.output

def test_ingest_meteocat(tmp_path):
    # Setup temporary catalog
    catalog_path = tmp_path / "catalog"
    dataset_dir = catalog_path / "datasets" / "meteocat-weather"
    dataset_dir.mkdir(parents=True)
    
    dataset_yml = dataset_dir / "dataset.yml"
    dataset_yml.write_text("""
id: meteocat-weather
name: Meteocat Weather
status: selected
""")

    output_dir = tmp_path / "output"
    
    result = runner.invoke(app, [
        "ingest", 
        "--dataset", "meteocat-weather", 
        "--catalog-path", str(catalog_path),
        "--output-dir", str(output_dir)
    ])
    
    assert result.exit_code == 0
    assert "Successfully ingested meteocat-weather" in result.output
    assert (output_dir / "landing").exists()
