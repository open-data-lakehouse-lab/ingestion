from abc import ABC, abstractmethod
from typing import Any, Dict
from pathlib import Path

class BaseWriter(ABC):
    @abstractmethod
    def write(self, payload: Dict[str, Any], dataset_id: str, output_dir: str, **kwargs: Any) -> Path:
        """Write payload to the target storage."""
        pass
