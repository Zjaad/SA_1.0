from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProgressBase(BaseModel):
    user_id: int
    subject_id: int
    completion_percentage: int = 0

class ProgressCreate(ProgressBase):
    pass

class ProgressUpdate(BaseModel):
    completion_percentage: Optional[int] = None

class Progress(ProgressBase):
    id: int
    last_studied: Optional[datetime]

    class Config:
        from_attributes = True
