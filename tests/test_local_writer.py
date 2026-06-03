import json
from pathlib import Path
from odl_ingestion.writers.local import LocalWriter
from datetime import datetime, timezone

def test_local_writer(tmp_path):
    writer = LocalWriter()
    payload = {"test": "data"}
    dataset_id = "meteocat-weather"
    output_dir = str(tmp_path / "data")
    
    output_path = writer.write(payload, dataset_id, output_dir)
    
    ingestion_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    expected_path = (
        Path(output_dir) / 
        "landing" / 
        "weather" / 
        "meteocat" / 
        dataset_id / 
        f"ingestion_date={ingestion_date}" / 
        "sample.json"
    )
    
    assert output_path == expected_path
    assert output_path.exists()
    
    with open(output_path, "r") as f:
        data = json.load(f)
        assert data == payload
