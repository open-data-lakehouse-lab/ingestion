import os
from typing import Optional
from pydantic import BaseModel

class Settings(BaseModel):
    catalog_path: str = os.getenv("CATALOG_PATH", "../datasets-catalog")
    output_dir: str = os.getenv("OUTPUT_DIR", "./data")
    meteocat_api_key: Optional[str] = os.getenv("METEOCAT_API_KEY", None)
    meteocat_base_url: str = os.getenv("METEOCAT_BASE_URL", "https://api.meteo.cat/xema/v1")
    meteocat_timeout_seconds: float = float(os.getenv("METEOCAT_TIMEOUT_SECONDS", "10.0"))
    meteocat_max_retries: int = int(os.getenv("METEOCAT_MAX_RETRIES", "2"))

settings = Settings()
