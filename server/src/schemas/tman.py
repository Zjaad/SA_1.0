from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class StudySession(BaseModel):
    subject: str
    start_time: datetime
    duration_minutes: int
    method: str
    break_duration: int
    priority: int
    energy_level_required: int

class ScheduleSuggestion(BaseModel):
    daily_schedule: List[StudySession]
    recommended_method: str
    expected_outcomes: List[str]
    breaks: List[Dict]
    total_study_time: int
    energy_management_tips: List[str]

class StudyPattern(BaseModel):
    best_time_slots: List[Dict]
    preferred_subjects: List[str]
    effective_methods: List[str]
    improvement_areas: List[str]
    success_patterns: Dict

class OptimizedSession(BaseModel):
    method: str
    duration: int
    steps: List[str]
    materials_needed: List[str]
    success_metrics: List[str]
