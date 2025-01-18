from sqlalchemy.orm import Session
from src.models.progress import Progress
from src.schemas.progress import ProgressCreate, ProgressUpdate
from datetime import datetime

class ProgressService:
    @staticmethod
    async def create_progress(db: Session, progress: ProgressCreate):
        db_progress = Progress(**progress.dict(), last_studied=datetime.now())
        db.add(db_progress)
        db.commit()
        db.refresh(db_progress)
        return db_progress

    @staticmethod
    async def get_user_progress(db: Session, user_id: int):
        return db.query(Progress).filter(Progress.user_id == user_id).all()

    @staticmethod
    async def update_progress(db: Session, user_id: int, subject_id: int, progress: ProgressUpdate):
        db_progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.subject_id == subject_id
        ).first()
        if db_progress:
            for key, value in progress.dict(exclude_unset=True).items():
                setattr(db_progress, key, value)
            db_progress.last_studied = datetime.now()
            db.commit()
            db.refresh(db_progress)
        return db_progress
