import httpx
import json
import time
from typing import Any, Dict, Optional
from ..base import BaseConnector
from ..errors import (
    ConnectorHttpError,
    ConnectorInvalidResponseError,
    ConnectorTimeoutError,
)
from ...config.settings import settings

class MeteocatConnector(BaseConnector):
    """
    Meteocat Weather API connector.
    """

    def __init__(self) -> None:
        super().__init__(dataset_id="meteocat-weather")
        self.base_url = settings.meteocat_base_url
        self.timeout = settings.meteocat_timeout_seconds
        self.max_retries = settings.meteocat_max_retries

    def _get_json(
        self, url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Helper to perform GET requests with retries, timeouts and error handling.
        """
        retries = 0
        while True:
            try:
                with httpx.Client() as client:
                    response = client.get(
                        url, headers=headers, params=params, timeout=self.timeout
                    )

                    if response.status_code == 200:
                        try:
                            return response.json()
                        except json.JSONDecodeError as e:
                            raise ConnectorInvalidResponseError(
                                f"Invalid JSON response from Meteocat API: {e}"
                            ) from e

                    # Check for transient errors
                    transient_status_codes = [429, 500, 502, 503, 504]
                    if response.status_code in transient_status_codes:
                        if retries < self.max_retries:
                            retries += 1
                            # Minimal sleep for retries
                            time.sleep(0.1)
                            continue

                    # Non-transient or exhausted retries
                    raise ConnectorHttpError(
                        f"Meteocat API returned HTTP {response.status_code} for URL: {url}"
                    )

            except httpx.TimeoutException as e:
                if retries < self.max_retries:
                    retries += 1
                    time.sleep(0.1)
                    continue
                raise ConnectorTimeoutError(f"Meteocat API request timed out: {e}") from e
            except httpx.RequestError as e:
                raise ConnectorHttpError(f"Error connecting to Meteocat API: {e}") from e

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

        data: Dict[str, Any] = self._get_json(url, headers=headers, params=params)
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

        data: Dict[str, Any] = self._get_json(url, headers=headers, params=params)
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

        data: Dict[str, Any] = self._get_json(url, headers=headers)
        return data
