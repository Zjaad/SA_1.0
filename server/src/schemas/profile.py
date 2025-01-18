from pydantic import BaseModel
from typing import Optional, Dict

class ProfileBase(BaseModel):
    study_level: str
    preferred_study_time: Dict
    daily_study_goal: int
    break_duration: int = 5
    session_duration: int = 25
    notification_enabled: bool = True
    theme_preference: str = "light"
    language_preference: str = "en"

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    study_level: Optional[str] = None
    preferred_study_time: Optional[Dict] = None
    daily_study_goal: Optional[int] = None
    break_duration: Optional[int] = None
    session_duration: Optional[int] = None
    notification_enabled: Optional[bool] = None
    theme_preference: Optional[str] = None
    language_preference: Optional[str] = None

class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
