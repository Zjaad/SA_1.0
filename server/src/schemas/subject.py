from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class SubjectLevel(str, Enum):
    PRIMARY = "primary"
    MIDDLE = "middle"
    HIGH_SCHOOL = "high_school"
    UNIVERSITY = "university"

class SubjectBase(BaseModel):
    name: str
    description: str
    level: str
    category: str
    language: str
    stream: str

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    stream: Optional[str] = None

class Subject(SubjectBase):
    id: int

    class Config:
        from_attributes = True
