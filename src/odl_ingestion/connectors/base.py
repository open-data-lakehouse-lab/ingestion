from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseConnector(ABC):
    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id

    @abstractmethod
    def extract_sample(self) -> Dict[str, Any]:
        """Extract a small sample payload for testing purposes."""
        pass
