from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from .user import User
from ..database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    study_level = Column(String)  # Current study level
    preferred_study_time = Column(JSON)  # Store time preferences as JSON
    daily_study_goal = Column(Integer)  # In minutes
    break_duration = Column(Integer)  # In minutes
    session_duration = Column(Integer)  # In minutes
    notification_enabled = Column(Boolean, default=True)
    theme_preference = Column(String, default="light")
    language_preference = Column(String, default="en")

    # Relationship
    user = relationship("User", back_populates="profile")
