from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.schemas.progress import Progress, ProgressCreate, ProgressUpdate
from src.services.progress import ProgressService
from src.services.auth import get_current_user

router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("", response_model=Progress)
async def create_progress(
    progress: ProgressCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ProgressService.create_progress(db, progress)

@router.get("/user/{user_id}", response_model=List[Progress])
async def get_user_progress(
    user_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ProgressService.get_user_progress(db, user_id)

@router.put("/{subject_id}", response_model=Progress)
async def update_progress(
    subject_id: int,
    progress: ProgressUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ProgressService.update_progress(db, current_user.id, subject_id, progress)
