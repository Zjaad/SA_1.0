from sqlalchemy.orm import Session
from src.models.profile import Profile
from src.schemas.profile import ProfileCreate, ProfileUpdate

class ProfileService:
    @staticmethod
    async def create_profile(db: Session, profile: ProfileCreate, user_id: int):
        db_profile = Profile(
            **profile.dict(),
            user_id=user_id
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    @staticmethod
    async def get_profile(db: Session, user_id: int):
        return db.query(Profile).filter(Profile.user_id == user_id).first()

    @staticmethod
    async def update_profile(db: Session, user_id: int, profile: ProfileUpdate):
        db_profile = await ProfileService.get_profile(db, user_id)
        if db_profile:
            for key, value in profile.dict(exclude_unset=True).items():
                setattr(db_profile, key, value)
            db.commit()
            db.refresh(db_profile)
        return db_profile
