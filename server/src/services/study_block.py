from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from src.models.study_block import StudyBlock
from src.schemas.study_block import StudyBlockCreate, StudyBlockUpdate

class StudyBlockService:
    @staticmethod
    async def create_study_block(db: Session, study_block: StudyBlockCreate):
        # Create basic study block
        db_block = StudyBlock(**study_block.dict())
        
        # Calculate initial focus score based on time of day and duration
        focus_score = await StudyBlockService._calculate_focus_score(
            db_block.start_time,
            db_block.end_time
        )
        db_block.focus_score = focus_score

        db.add(db_block)
        db.commit()
        db.refresh(db_block)
        return db_block

    @staticmethod
    async def get_study_block(db: Session, block_id: int):
        return db.query(StudyBlock).filter(StudyBlock.id == block_id).first()

    @staticmethod
    async def get_schedule_blocks(
        db: Session, 
        schedule_id: int,
        skip: int = 0,
        limit: int = 100
    ):
        return db.query(StudyBlock)\
            .filter(StudyBlock.schedule_id == schedule_id)\
            .order_by(StudyBlock.start_time)\
            .offset(skip)\
            .limit(limit)\
            .all()

    @staticmethod
    async def update_study_block(
        db: Session, 
        block_id: int, 
        study_block: StudyBlockUpdate
    ):
        db_block = await StudyBlockService.get_study_block(db, block_id)
        if db_block:
            # Update basic fields
            for key, value in study_block.dict(exclude_unset=True).items():
                setattr(db_block, key, value)
            
            # Recalculate focus score if timing changed
            if 'start_time' in study_block.dict(exclude_unset=True) or \
               'end_time' in study_block.dict(exclude_unset=True):
                focus_score = await StudyBlockService._calculate_focus_score(
                    db_block.start_time,
                    db_block.end_time
                )
                db_block.focus_score = focus_score

            db.commit()
            db.refresh(db_block)
        return db_block

    @staticmethod
    async def delete_study_block(db: Session, block_id: int):
        db_block = await StudyBlockService.get_study_block(db, block_id)
        if db_block:
            db.delete(db_block)
            db.commit()
        return db_block

    @staticmethod
    async def complete_study_block(
        db: Session, 
        block_id: int, 
        efficiency_rating: Optional[int] = None
    ):
        """Mark a study block as completed and record efficiency"""
        db_block = await StudyBlockService.get_study_block(db, block_id)
        if db_block:
            db_block.is_completed = True
            if efficiency_rating is not None:
                db_block.efficiency_rating = efficiency_rating
            db.commit()
            db.refresh(db_block)
        return db_block

    @staticmethod
    async def get_optimal_study_blocks(
        db: Session,
        schedule_id: int,
        date: datetime
    ) -> List[StudyBlock]:
        """Get AI-optimized study blocks for a specific day"""
        # Get all blocks for the day
        blocks = db.query(StudyBlock)\
            .filter(StudyBlock.schedule_id == schedule_id)\
            .filter(
                StudyBlock.start_time >= date,
                StudyBlock.start_time < date + timedelta(days=1)
            )\
            .all()

        # TODO: Apply AI optimization
        # This will be integrated with Tman's AI recommendations
        return blocks

    @staticmethod
    async def _calculate_focus_score(
        start_time: datetime,
        end_time: datetime
    ) -> int:
        """
        Calculate a focus score for a study block based on various factors.
        This is a placeholder for the actual AI-based calculation.
        """
        # TODO: Integrate with AI service for more sophisticated scoring
        hour = start_time.hour
        duration = (end_time - start_time).total_seconds() / 3600  # in hours

        # Basic scoring based on time of day
        base_score = 70  # Base score out of 100
        
        # Time of day adjustment
        if 8 <= hour <= 11:  # Morning
            base_score += 20
        elif 14 <= hour <= 17:  # Afternoon
            base_score += 10
        elif 19 <= hour <= 22:  # Evening
            base_score += 5
        
        # Duration adjustment
        if duration <= 1.5:  # Optimal duration
            base_score += 10
        elif duration > 2:  # Too long
            base_score -= 10

        return min(100, max(0, base_score))  # Ensure score is between 0 and 100
