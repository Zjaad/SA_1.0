from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.services.profile import ProfileService
from src.services.auth import get_current_user
from src.schemas.profile import Profile, ProfileCreate, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])

@router.post("", response_model=Profile)
async def create_profile(
    profile: ProfileCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ProfileService.create_profile(db, profile, current_user.id)

@router.get("", response_model=Profile)
async def get_profile(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = await ProfileService.get_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("", response_model=Profile)
async def update_profile(
    profile: ProfileUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ProfileService.update_profile(db, current_user.id, profile)
