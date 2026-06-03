from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class DatasetMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")
    
    id: str
    name: str
    description: Optional[str] = None
    status: str
    license: Any = None
    source_url: Optional[str] = None
    domain: Optional[str] = None
    category: Optional[str] = None
    format: Any = None
