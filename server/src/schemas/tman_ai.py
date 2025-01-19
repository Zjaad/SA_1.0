from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class EnergyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Request Schemas
class PatternAnalysisRequest(BaseModel):
    study_history: List[Dict]
    start_date: datetime
    end_date: datetime
    subjects: List[str]

class ScheduleOptimizationRequest(BaseModel):
    schedule_data: Dict = Field(..., description="Current schedule data")
    performance_data: Dict = Field(..., description="User's performance metrics")
    preferences: Dict = Field(default={}, description="User scheduling preferences")
    constraints: Optional[Dict] = None

class StudyMethodRequest(BaseModel):
    subject: str
    topic: str
    context: Dict = Field(..., description="Study context including time, energy level, etc.")
    previous_methods: Optional[List[str]] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)

class SmartBreakRequest(BaseModel):
    study_duration: int = Field(..., description="Duration in minutes")
    energy_level: EnergyLevel
    last_break: datetime
    activity_preferences: Optional[List[str]] = None

# Response Schemas
class StudyPattern(BaseModel):
    best_times: List[str]
    effective_methods: List[str]
    improvement_areas: List[str]
    recommendations: List[str]
    confidence_score: float = Field(..., ge=0, le=1)

class PatternAnalysisResponse(BaseModel):
    patterns: StudyPattern
    insights: List[str]
    suggestions: List[str]

class ScheduleBlock(BaseModel):
    subject: str
    start_time: datetime
    duration: int
    method: str
    energy_required: EnergyLevel
    break_after: Optional[int] = None

class OptimizedSchedule(BaseModel):
    blocks: List[ScheduleBlock]
    breaks: List[Dict]
    estimated_effectiveness: float
    recommendations: List[str]
    adaptations: List[Dict]

class StudyMethodSuggestion(BaseModel):
    recommended_method: str
    reason: str
    implementation_steps: List[str]
    estimated_effectiveness: float
    alternatives: List[str]
    tips: List[str]

class SmartBreakSuggestion(BaseModel):
    duration: int
    suggested_time: datetime
    activity: str
    reason: str
    energy_impact: str
    alternatives: List[str]

# Example Usage Response
class ExampleResponse(BaseModel):
    """Example responses for documentation"""
    pattern_analysis = {
        "patterns": {
            "best_times": ["09:00-11:00", "15:00-17:00"],
            "effective_methods": ["pomodoro", "active_recall"],
            "improvement_areas": ["break consistency", "evening focus"],
            "recommendations": [
                "Start difficult subjects in the morning",
                "Take more consistent breaks"
            ],
            "confidence_score": 0.85
        },
        "insights": [
            "Higher performance in morning sessions",
            "Better retention with active recall"
        ],
        "suggestions": [
            "Implement 5-minute breaks every 25 minutes",
            "Use mornings for challenging topics"
        ]
    }


# The new response classes ... tman is smart <3

class FocusAnalysis(BaseModel):
    """Analysis of student's focus and attention"""
    peak_focus_hours: List[str]
    attention_span: int  # in minutes
    distraction_patterns: List[str]
    focus_improvement_tips: List[str]
    recommended_break_frequency: int  # in minutes

class MethodEffectiveness(BaseModel):
    """Analysis of study method effectiveness"""
    method_name: str
    effectiveness_score: float
    strengths: List[str]
    weaknesses: List[str]
    best_subjects: List[str]
    improvement_suggestions: List[str]

class LearningProgress(BaseModel):
    """Detailed learning progress analysis"""
    mastery_level: float  # 0 to 1
    weak_areas: List[str]
    strong_areas: List[str]
    revision_needed: List[str]
    next_steps: List[str]
    estimated_time_to_mastery: int  # in hours

class PersonalizedTips(BaseModel):
    """AI-generated personalized study tips"""
    daily_tips: List[str]
    subject_specific_tips: Dict[str, List[str]]
    energy_management_tips: List[str]
    motivation_boosters: List[str]

class StudyStreak(BaseModel):
    """Study streak and motivation tracking"""
    current_streak: int  # in days
    longest_streak: int
    total_study_hours: float
    achievements: List[str]
    next_milestone: str
    motivation_score: float  # 0 to 1

class ComprehensiveReport(BaseModel):
    """Complete analysis combining multiple metrics"""
    focus_analysis: FocusAnalysis
    method_effectiveness: List[MethodEffectiveness]
    learning_progress: LearningProgress
    personalized_tips: PersonalizedTips
    study_streak: StudyStreak
    overall_score: float
    recommendations: List[str]
