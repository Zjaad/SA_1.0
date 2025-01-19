from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.database import get_db
from src.schemas.study_block import StudyBlock, StudyBlockCreate, StudyBlockUpdate
from src.services.study_block import StudyBlockService
from src.services.auth import get_current_user

router = APIRouter(prefix="/study-blocks", tags=["study-blocks"])

@router.post("", response_model=StudyBlock)
async def create_study_block(
    study_block: StudyBlockCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await StudyBlockService.create_study_block(db, study_block)

@router.get("/schedule/{schedule_id}", response_model=List[StudyBlock])
async def get_schedule_blocks(
    schedule_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await StudyBlockService.get_schedule_blocks(db, schedule_id, skip, limit)

@router.get("/{block_id}", response_model=StudyBlock)
async def get_study_block(
    block_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    block = await StudyBlockService.get_study_block(db, block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Study block not found")
    return block

@router.put("/{block_id}", response_model=StudyBlock)
async def update_study_block(
    block_id: int,
    study_block: StudyBlockUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_block = await StudyBlockService.get_study_block(db, block_id)
    if not existing_block:
        raise HTTPException(status_code=404, detail="Study block not found")
    return await StudyBlockService.update_study_block(db, block_id, study_block)

@router.post("/{block_id}/complete")
async def complete_study_block(
    block_id: int,
    efficiency_rating: int = Query(None, ge=1, le=5),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    block = await StudyBlockService.complete_study_block(db, block_id, efficiency_rating)
    if not block:
        raise HTTPException(status_code=404, detail="Study block not found")
    return block

@router.get("/optimal/{schedule_id}", response_model=List[StudyBlock])
async def get_optimal_blocks(
    schedule_id: int,
    date: datetime,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await StudyBlockService.get_optimal_study_blocks(db, schedule_id, date)
