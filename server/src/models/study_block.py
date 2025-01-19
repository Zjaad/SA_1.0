from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum

class StudyMethodType(enum.Enum):
   # Time Management Methods
   POMODORO = "pomodoro"                # 25min work, 5min break
   TIMEBOXING = "timeboxing"            # Fixed time blocks
   
   # Active Learning Methods
   ACTIVE_RECALL = "active_recall"      # Self-testing
   FEYNMAN = "feynman"                  # Teaching to understand
   BLURTING = "blurting"                # Writing everything you know
   PEER_TEACHING = "peer_teaching"      # Teaching others
   
   # Visualization Methods
   MIND_MAPPING = "mind_mapping"        # Visual connections
   FLOWCHARTS = "flowcharts"            # Process visualization
   CONCEPT_MAPPING = "concept_mapping"  # Ideas connection
   MEMORY_PALACE = "memory_palace"      # Visualization technique
   
   # Reading & Note-taking Methods
   SQ3R = "sq3r"                        # Survey, Question, Read, Recite, Review
   CORNELL_NOTES = "cornell_notes"      # Systematic note-taking
   PQ4R = "pq4r"                        # Preview, Question, Read, Reflect, Recite, Review
   
   # Organization Methods
   CHUNKING = "chunking"                # Breaking info into pieces
   INTERLEAVING = "interleaving"        # Mixed practice
   SPACED_REPETITION = "spaced_rep"     # Timed review intervals
   
   # Practice Methods
   PRACTICE_TESTING = "practice_test"   # Self-assessment
   QUESTION_GEN = "question_gen"        # Creating test questions
   PROBLEM_SOLVING = "problem_solving"  # Working through problems

class EnergyLevel(enum.Enum):
   HIGH = "high"
   MEDIUM = "medium"
   LOW = "low"

class StudyBlock(Base):
   __tablename__ = "study_blocks"

   # Basic Fields
   id = Column(Integer, primary_key=True, index=True)
   schedule_id = Column(Integer, ForeignKey("schedules.id"))
   subject_id = Column(Integer, ForeignKey("subjects.id"))
   start_time = Column(DateTime(timezone=True))
   end_time = Column(DateTime(timezone=True))
   priority = Column(Integer)  # 1-5 priority level
   
   # Status & Ratings
   is_completed = Column(Boolean, default=False)
   efficiency_rating = Column(Integer)  # User feedback
   focus_score = Column(Integer)  # AI-generated score
   notes = Column(String)

   # Smart Features
   energy_level = Column(Enum(EnergyLevel), default=EnergyLevel.MEDIUM)
   study_method = Column(Enum(StudyMethodType))
   
   # Learning Analytics
   learning_metrics = Column(JSON, default={
       "retention_score": 0,
       "understanding_level": 0,
       "difficulty_rating": 0,
       "attention_span": 0,
       "comprehension_rate": 0
   })

   # Session Management
   break_schedule = Column(JSON, default={
       "intervals": [],
       "durations": [],
       "activities": []
   })

   # Progress Tracking
   progress_metrics = Column(JSON, default={
       "milestones": [],
       "challenges": [],
       "achievements": [],
       "focus_duration": 0,
       "distraction_count": 0
   })

   # Environmental Context
   study_context = Column(JSON, default={
       "location": "home",
       "noise_level": "low",
       "lighting": "good",
       "temperature": "optimal"
   })

   # AI Adaptations
   ai_suggestions = Column(JSON, default={
       "method_adjustments": [],
       "timing_adjustments": [],
       "break_adjustments": [],
       "environment_recommendations": []
   })

   # Timestamps
   created_at = Column(DateTime(timezone=True), server_default=func.now())
   updated_at = Column(DateTime(timezone=True), onupdate=func.now())

   # Relationships
   schedule = relationship("Schedule", back_populates="study_blocks")
   subject = relationship("Subject", back_populates="study_blocks")

   # Helper Methods
   @property
   def duration_minutes(self):
       """Calculate duration in minutes"""
       if self.start_time and self.end_time:
           return int((self.end_time - self.start_time).total_seconds() / 60)
       return 0

   @property
   def effectiveness_score(self):
       """Calculate overall effectiveness"""
       if not self.is_completed:
           return 0
       
       weights = {
           'efficiency_rating': 0.3,
           'focus_score': 0.3,
           'retention_score': 0.4
       }
       
       return (
           weights['efficiency_rating'] * self.efficiency_rating +
           weights['focus_score'] * self.focus_score +
           weights['retention_score'] * self.learning_metrics['retention_score']
       )

   def suggest_break(self) -> dict:
       """Get smart break suggestions"""
       return {
           "timing": self.duration_minutes // 2,
           "duration": 5 if self.duration_minutes < 45 else 10,
           "activity": "stretch" if self.energy_level == EnergyLevel.LOW else "walk"
       }

   def update_metrics(self, new_metrics: dict):
       """Update learning metrics"""
       self.learning_metrics.update(new_metrics)

   def get_optimal_method(self) -> StudyMethodType:
       """Determine best study method based on context"""
       # To be implemented with AI
       pass
