import httpx
from typing import Any, Dict, Optional
from ..base import BaseConnector
from ...config.settings import settings

class MeteocatConnector(BaseConnector):
    """
    Meteocat Weather API connector.
    """

    def __init__(self) -> None:
        super().__init__(dataset_id="meteocat-weather")
        self.base_url = settings.meteocat_base_url

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

    def extract_station_metadata(
        self,
        api_key: str,
        station_status: str = "all",
        metadata_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Extract station metadata from Meteocat API.
        """
        url = f"{self.base_url}/estacions/metadades"
        headers = {"x-api-key": api_key}
        params = {}
        if station_status and station_status != "all":
            params["estat"] = station_status
        if metadata_date:
            params["data"] = metadata_date

        with httpx.Client() as client:
            response = client.get(url, headers=headers, params=params, timeout=10.0)
            response.raise_for_status()
            data: Dict[str, Any] = response.json()
            return data

    def extract_measured_variable(
        self,
        api_key: str,
        variable_code: str,
        year: int,
        month: int,
        day: int,
        station_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Extract measured variable data from Meteocat API.
        """
        url = f"{self.base_url}/variables/mesurades/{variable_code}/{year}/{month}/{day}"
        headers = {"x-api-key": api_key}
        params = {}
        if station_code:
            params["codiEstacio"] = station_code

        with httpx.Client() as client:
            response = client.get(url, headers=headers, params=params, timeout=10.0)
            response.raise_for_status()
            data: Dict[str, Any] = response.json()
            return data

    def extract_variables_metadata(
        self,
        api_key: str,
    ) -> Dict[str, Any]:
        """
        Extract variables metadata from Meteocat API.
        """
        url = f"{self.base_url}/variables/auxiliars/metadades"
        headers = {"x-api-key": api_key}

        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10.0)
            response.raise_for_status()
            data: Dict[str, Any] = response.json()
            return data
