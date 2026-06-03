import pytest
import yaml
from odl_ingestion.catalog.loader import CatalogLoader

def test_list_datasets(tmp_path):
    # Create a temporary catalog structure
    catalog_dir = tmp_path / "catalog"
    datasets_dir = catalog_dir / "datasets" / "weather" / "meteocat-weather"
    datasets_dir.mkdir(parents=True)
    
    dataset_data = {
        "id": "meteocat-weather",
        "name": "Meteocat Weather",
        "description": "Weather data from Meteocat",
        "status": "selected",
        "license": "CC-BY-4.0",
        "category": "weather",
        "format": "json"
    }
    
    with open(datasets_dir / "dataset.yml", "w") as f:
        yaml.dump(dataset_data, f)
        
    loader = CatalogLoader(str(catalog_dir))
    datasets = loader.list_datasets()
    
    assert len(datasets) == 1
    assert datasets[0].id == "meteocat-weather"
    assert datasets[0].name == "Meteocat Weather"

def test_get_dataset(tmp_path):
    catalog_dir = tmp_path / "catalog"
    datasets_dir = catalog_dir / "datasets" / "weather" / "meteocat-weather"
    datasets_dir.mkdir(parents=True)
    
    dataset_data = {
        "id": "meteocat-weather",
        "name": "Meteocat Weather",
        "description": "Weather data from Meteocat",
        "status": "selected",
        "license": "CC-BY-4.0",
        "category": "weather",
        "format": "json"
    }
    
    with open(datasets_dir / "dataset.yml", "w") as f:
        yaml.dump(dataset_data, f)
        
    loader = CatalogLoader(str(catalog_dir))
    ds = loader.get_dataset("meteocat-weather")
    
    assert ds.id == "meteocat-weather"
    
    with pytest.raises(ValueError, match="not found in catalog"):
        loader.get_dataset("non-existent")
