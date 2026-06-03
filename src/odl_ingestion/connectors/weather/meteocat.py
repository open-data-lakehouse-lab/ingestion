from typing import Any, Dict
from ..base import BaseConnector

class MeteocatConnector(BaseConnector):
    """
    Skeleton for Meteocat Weather API connector.
    
    TODO:
    - API endpoint selection (e.g., current weather, forecasts).
    - API Key handling through environment variables (METEOCAT_API_KEY).
    - Pagination or date partitioning if needed.
    - Error handling for API limits and network issues.
    - Rate limit handling.
    - Schema mapping to internal models.
    """

    def __init__(self) -> None:
        super().__init__(dataset_id="meteocat-weather")

    def extract_sample(self) -> Dict[str, Any]:
        """
        Returns a small in-memory sample payload.
        No real API calls are made here.
        """
        return {
            "metadata": {
                "source": "meteocat",
                "dataset": self.dataset_id,
                "is_sample": True,
                "version": "1.0"
            },
            "data": [
                {
                    "station_id": "D5",
                    "station_name": "Barcelona - El Raval",
                    "temperature": 22.5,
                    "humidity": 65,
                    "timestamp": "2026-06-03T13:00:00Z"
                }
            ]
        }
