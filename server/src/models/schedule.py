from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum

class ScheduleType(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    EXAM_PREP = "exam_prep"
    REVISION = "revision"
    CUSTOM = "custom"

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    schedule_type = Column(Enum(ScheduleType), default=ScheduleType.DAILY)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    # Smart Features
    preferences = Column(JSON)  # Store user preferences as JSON
    ai_suggestions = Column(JSON)  # Store AI recommendations
    
    # Learning Analytics
    energy_patterns = Column(JSON, default={
        "peak_hours": [],
        "medium_hours": [],
        "low_hours": [],
        "break_preferences": {}
    })
    
    performance_metrics = Column(JSON, default={
        "completion_rate": 0,
        "focus_scores": [],
        "break_adherence": 0,
        "productivity_patterns": {}
    })
    
    adaptation_history = Column(JSON, default={
        "schedule_changes": [],
        "success_patterns": {},
        "improvement_areas": []
    })

    # Time Management
    study_goals = Column(JSON, default={
        "daily_hours": 0,
        "subject_priorities": {},
        "target_scores": {}
    })

    optimization_rules = Column(JSON, default={
        "subject_order": [],
        "break_patterns": {},
        "difficulty_distribution": {},
        "revision_frequency": {}
    })

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="schedules")
    study_blocks = relationship("StudyBlock", back_populates="schedule")

    @property
    def is_active(self):
        """Check if schedule is currently active"""
        current_time = func.now()
        return self.start_date <= current_time <= self.end_date

    @property
    def completion_rate(self):
        """Calculate schedule completion rate"""
        completed = sum(1 for block in self.study_blocks if block.is_completed)
        total = len(self.study_blocks)
        return (completed / total * 100) if total > 0 else 0

    @property
    def next_study_block(self):
        """Get the next upcoming study block"""
        current_time = func.now()
        return next(
            (block for block in self.study_blocks 
             if block.start_time > current_time and not block.is_completed),
            None
        )

    def update_energy_patterns(self, new_patterns):
        """Update energy patterns based on user performance"""
        self.energy_patterns.update(new_patterns)

    def add_performance_metric(self, metric_type, value):
        """Add new performance metric"""
        if metric_type not in self.performance_metrics:
            self.performance_metrics[metric_type] = []
        self.performance_metrics[metric_type].append({
            "value": value,
            "timestamp": func.now()
        })

    def suggest_schedule_adjustment(self):
        """Generate schedule adjustment suggestions"""
        # This will be enhanced with AI
        adjustments = {
            "suggested_changes": [],
            "reason": "",
            "expected_improvement": 0
        }
        return adjustments
