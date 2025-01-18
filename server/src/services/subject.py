from sqlalchemy.orm import Session
from src.models.subject import Subject
from src.schemas.subject import SubjectCreate, SubjectUpdate

class SubjectService:
    @staticmethod
    async def create_subject(db: Session, subject: SubjectCreate):
        db_subject = Subject(**subject.dict())
        db.add(db_subject)
        db.commit()
        db.refresh(db_subject)
        return db_subject

    @staticmethod
    async def get_subject(db: Session, subject_id: int):
        return db.query(Subject).filter(Subject.id == subject_id).first()

    @staticmethod
    async def get_subjects(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        level: str = None,
        category: str = None
    ):
        query = db.query(Subject)
        if level:
            query = query.filter(Subject.level == level)
        if category:
            query = query.filter(Subject.category == category)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    async def update_subject(db: Session, subject_id: int, subject: SubjectUpdate):
        db_subject = await SubjectService.get_subject(db, subject_id)
        if db_subject:
            for key, value in subject.dict(exclude_unset=True).items():
                setattr(db_subject, key, value)
            db.commit()
            db.refresh(db_subject)
        return db_subject
