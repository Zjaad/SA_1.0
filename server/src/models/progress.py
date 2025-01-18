from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    completion_percentage = Column(Integer, default=0)
    last_studied = Column(DateTime(timezone=True), default=func.now())
    
    user = relationship("User", back_populates="progress_records")
    subject = relationship("Subject", back_populates="progress_records")
