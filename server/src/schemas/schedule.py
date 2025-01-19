from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class ScheduleBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    preferences: Dict = {}  # For storing user preferences
    ai_suggestions: Optional[Dict] = {}  # For AI recommendations

class ScheduleCreate(ScheduleBase):
    user_id: int

class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    preferences: Optional[Dict] = None
    ai_suggestions: Optional[Dict] = None

class Schedule(ScheduleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
