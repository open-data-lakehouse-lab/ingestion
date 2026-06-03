import yaml
from pathlib import Path
from typing import List
from .models import DatasetMetadata

class CatalogLoader:
    def __init__(self, catalog_path: str):
        self.catalog_path = Path(catalog_path)

    def list_datasets(self) -> List[DatasetMetadata]:
        datasets = []
        # Search for dataset.yml files in any subdirectory of 'datasets'
        datasets_root = self.catalog_path / "datasets"
        if not datasets_root.exists():
            return []
            
        for yaml_file in datasets_root.glob("**/dataset.yml"):
            with open(yaml_file, "r") as f:
                data = yaml.safe_load(f)
                datasets.append(DatasetMetadata(**data))
        return datasets

    def get_dataset(self, dataset_id: str) -> DatasetMetadata:
        datasets = self.list_datasets()
        for ds in datasets:
            if ds.id == dataset_id:
                return ds
        raise ValueError(f"Dataset with ID '{dataset_id}' not found in catalog.")
