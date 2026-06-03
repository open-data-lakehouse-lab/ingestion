import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
from .base import BaseWriter

class LocalWriter(BaseWriter):
    def write(self, payload: Dict[str, Any], dataset_id: str, output_dir: str) -> Path:
        # For this MVP, we assume a specific structure for meteocat
        # In a real scenario, this would be more dynamic based on dataset metadata
        
        category = "weather"
        source = "meteocat"
        
        ingestion_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        target_path = (
            Path(output_dir) / 
            "landing" / 
            category / 
            source / 
            dataset_id / 
            f"ingestion_date={ingestion_date}" / 
            "sample.json"
        )
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(target_path, "w") as f:
            json.dump(payload, f, indent=2)
            
        return target_path
