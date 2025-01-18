from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.database import get_db
from src.schemas.subject import Subject, SubjectCreate, SubjectUpdate
from src.services.subject import SubjectService
from src.services.auth import get_current_user

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.post("", response_model=Subject)
async def create_subject(
    subject: SubjectCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await SubjectService.create_subject(db, subject)

@router.get("", response_model=List[Subject])
async def get_subjects(
    skip: int = 0,
    limit: int = 100,
    level: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return await SubjectService.get_subjects(db, skip, limit, level, category)

@router.get("/{subject_id}", response_model=Subject)
async def get_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):
    subject = await SubjectService.get_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.put("/{subject_id}", response_model=Subject)
async def update_subject(
    subject_id: int,
    subject: SubjectUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_subject = await SubjectService.update_subject(db, subject_id, subject)
    if not updated_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return updated_subject
