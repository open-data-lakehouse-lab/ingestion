import os
from typing import Optional
from pydantic import BaseModel

class Settings(BaseModel):
    catalog_path: str = os.getenv("CATALOG_PATH", "../datasets-catalog")
    output_dir: str = os.getenv("OUTPUT_DIR", "./data")
    meteocat_api_key: Optional[str] = os.getenv("METEOCAT_API_KEY", None)
    meteocat_base_url: str = os.getenv("METEOCAT_BASE_URL", "https://api.meteo.cat/xema/v1")

settings = Settings()
