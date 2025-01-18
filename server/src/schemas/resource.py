from pydantic import BaseModel
from typing import Optional

class ResourceBase(BaseModel):
    title: str
    type: str
    content: str
    language: str
    subject_id: int

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    content: Optional[str] = None
    language: Optional[str] = None

class Resource(ResourceBase):
    id: int

    class Config:
        from_attributes = True
