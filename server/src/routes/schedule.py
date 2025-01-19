from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.schemas.schedule import Schedule, ScheduleCreate, ScheduleUpdate
from src.services.schedule import ScheduleService
from src.services.auth import get_current_user
from src.models.user import User  

router = APIRouter(prefix="/schedules", tags=["schedules"])

@router.post("", response_model=Schedule)
async def create_schedule(
    schedule: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ScheduleService.create_schedule(db, schedule)

@router.get("/{schedule_id}", response_model=Schedule)
async def get_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),  # Change type hint to User
    db: Session = Depends(get_db)
):
    schedule = await ScheduleService.get_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if schedule.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this schedule")
    return schedule
@router.put("/{schedule_id}", response_model=Schedule)
async def update_schedule(
    schedule_id: int,
    schedule: ScheduleUpdate,
    current_user: User = Depends(get_current_user),  # Change type hint to User
    db: Session = Depends(get_db)
):
    existing_schedule = await ScheduleService.get_schedule(db, schedule_id)
    if not existing_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if existing_schedule.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this schedule")
    return await ScheduleService.update_schedule(db, schedule_id, schedule)
