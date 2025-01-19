from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    schedule_time: datetime
    type: str
    data: Optional[Dict] = None

class Notification(NotificationCreate):
    id: int
    created_at: datetime
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NotificationPreferences(BaseModel):
    study_start: bool = True
    break_time: bool = True
    review_due: bool = True
    energy_check: bool = True
    daily_summary: bool = True
    study_end: bool = True
    goal_achieved: bool = True
    streak_update: bool = True
    low_energy_warning: bool = True
    schedule_change: bool = True
    exam_reminder: bool = True
    motivation_boost: bool = True
    weekly_report: bool = True
    
    # Timing preferences
    advance_notice_minutes: int = 5
    quiet_hours_start: str = "22:00"
    quiet_hours_end: str = "07:00"
    preferred_channels: List[str] = ["app", "email"]

    # Frequency settings
    energy_check_frequency: str = "hourly"
    summary_frequency: str = "daily"
    motivation_frequency: str = "daily"

class UserNotificationSettings(BaseModel):
    user_id: int
    preferences: NotificationPreferences
    enabled: bool = True
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
