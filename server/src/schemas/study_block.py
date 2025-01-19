from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StudyBlockBase(BaseModel):
    schedule_id: int
    subject_id: int
    start_time: datetime
    end_time: datetime
    priority: int
    focus_score: Optional[int] = None
    notes: Optional[str] = None

class StudyBlockCreate(StudyBlockBase):
    pass

class StudyBlockUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    priority: Optional[int] = None
    is_completed: Optional[bool] = None
    efficiency_rating: Optional[int] = None
    focus_score: Optional[int] = None
    notes: Optional[str] = None

class StudyBlock(StudyBlockBase):
    id: int
    is_completed: bool
    efficiency_rating: Optional[int] = None

    class Config:
        from_attributes = True
