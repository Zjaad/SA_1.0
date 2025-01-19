from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from src.models.schedule import Schedule
from src.schemas.schedule import ScheduleCreate, ScheduleUpdate
from src.services.auth import get_current_user

class ScheduleService:
    @staticmethod
    async def create_schedule(db: Session, schedule: ScheduleCreate):
        # Create basic schedule
        db_schedule = Schedule(**schedule.dict())
        
        # Add AI-generated suggestions
        ai_suggestions = await ScheduleService._generate_ai_suggestions(
            schedule.start_date,
            schedule.end_date,
            schedule.preferences
        )
        db_schedule.ai_suggestions = ai_suggestions

        db.add(db_schedule)
        db.commit()
        db.refresh(db_schedule)
        return db_schedule

    @staticmethod
    async def get_schedule(db: Session, schedule_id: int):
        return db.query(Schedule).filter(Schedule.id == schedule_id).first()

    @staticmethod
    async def get_user_schedules(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ):
        return db.query(Schedule)\
            .filter(Schedule.user_id == user_id)\
            .offset(skip)\
            .limit(limit)\
            .all()

    @staticmethod
    async def update_schedule(
        db: Session, 
        schedule_id: int, 
        schedule: ScheduleUpdate
    ):
        db_schedule = await ScheduleService.get_schedule(db, schedule_id)
        if db_schedule:
            # Update basic fields
            for key, value in schedule.dict(exclude_unset=True).items():
                if key != 'ai_suggestions':  # Don't directly update AI suggestions
                    setattr(db_schedule, key, value)
            
            # If schedule timing changed, regenerate AI suggestions
            if 'start_date' in schedule.dict(exclude_unset=True) or \
               'end_date' in schedule.dict(exclude_unset=True):
                ai_suggestions = await ScheduleService._generate_ai_suggestions(
                    db_schedule.start_date,
                    db_schedule.end_date,
                    db_schedule.preferences
                )
                db_schedule.ai_suggestions = ai_suggestions

            db.commit()
            db.refresh(db_schedule)
        return db_schedule

    @staticmethod
    async def delete_schedule(db: Session, schedule_id: int):
        db_schedule = await ScheduleService.get_schedule(db, schedule_id)
        if db_schedule:
            db.delete(db_schedule)
            db.commit()
        return db_schedule

    @staticmethod
    async def optimize_schedule(db: Session, schedule_id: int):
        """Optimize an existing schedule using AI"""
        db_schedule = await ScheduleService.get_schedule(db, schedule_id)
        if db_schedule:
            # Generate new AI suggestions based on current data
            ai_suggestions = await ScheduleService._generate_ai_suggestions(
                db_schedule.start_date,
                db_schedule.end_date,
                db_schedule.preferences,
                include_performance_data=True
            )
            db_schedule.ai_suggestions = ai_suggestions
            db.commit()
            db.refresh(db_schedule)
        return db_schedule

    @staticmethod
    async def _generate_ai_suggestions(
        start_date: datetime,
        end_date: datetime,
        preferences: dict,
        include_performance_data: bool = False
    ) -> dict:
        """
        Generate AI suggestions for schedule optimization.
        This is a placeholder for the actual AI integration.
        """
        # TODO: Integrate with actual AI service
        return {
            "recommended_study_times": {
                "morning": ["08:00", "10:00"],
                "afternoon": ["14:00", "16:00"],
                "evening": ["19:00", "21:00"]
            },
            "break_recommendations": {
                "frequency": "every 45 minutes",
                "duration": "15 minutes"
            },
            "subject_order": [
                "high_focus_subjects",
                "medium_focus_subjects",
                "low_focus_subjects"
            ],
            "daily_study_limit": "6 hours",
            "personalized_tips": [
                "Schedule difficult subjects during your peak energy hours",
                "Take longer breaks after intense study sessions",
                "Review material from previous day before starting new topics"
            ]
        }
