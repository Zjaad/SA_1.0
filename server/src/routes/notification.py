# src/routes/notification.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from datetime import datetime, timedelta
from src.services.auth import get_current_user
from src.models.user import User

router = APIRouter(prefix="/notifications", tags=["notifications"])
notification_service = StudyNotificationService()

@router.post("/schedule-study")
async def schedule_study_notifications(
    subject: str,
    topic: str,
    start_time: datetime,
    duration: int,
    current_user: User = Depends(get_current_user)
):
    """Schedule notifications for a study session"""
    notifications = await notification_service.schedule_study_session(
        current_user.id,
        subject,
        topic,
        start_time,
        duration
    )
    return {"notifications": notifications}

@router.post("/schedule-exam")
async def schedule_exam_notifications(
    subject: str,
    exam_date: datetime,
    current_user: User = Depends(get_current_user)
):
    """Schedule exam reminder notifications"""
    notifications = await notification_service.schedule_exam_reminder(
        current_user.id,
        subject,
        exam_date
    )
    return {"notifications": notifications}

@router.post("/schedule-review")
async def schedule_review_notifications(
    subject: str,
    topic: str,
    study_date: datetime,
    current_user: User = Depends(get_current_user)
):
    """Schedule review reminder notifications"""
    notifications = await notification_service.schedule_review_reminder(
        current_user.id,
        subject,
        topic,
        study_date
    )
    return {"notifications": notifications}
