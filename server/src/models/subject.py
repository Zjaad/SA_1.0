from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from ..database import Base

class SubjectLevel(str, PyEnum):
    PRIMARY = "primary"
    MIDDLE = "middle"
    HIGH_SCHOOL = "high_school"
    UNIVERSITY = "university"

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    level = Column(String)  # e.g., "1BAC", "2BAC", etc.
    category = Column(String)  # e.g., "Science", "Math", "Literature"
    language = Column(String)  # For multilingual support
    stream = Column(String)  # e.g., "Science Math", "Science Physique"

    #another relationship definitions
    resources = relationship("Resource", back_populates="subject")
    progress_records = relationship("Progress", back_populates="subject")
