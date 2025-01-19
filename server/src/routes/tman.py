from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
from src.database import get_db
from src.services.Tman_service import TmanAI
from src.services.auth import get_current_user
from src.models.user import User

router = APIRouter(prefix="/tman", tags=["time-management-ai"])

# Initialize Tman
tman = TmanAI()

@router.post("/generate-schedule")
async def generate_schedule(
    student_data: Dict,
    available_time: Dict,
    subjects: List[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate personalized study schedule suggestions"""
    try:
        schedules = await tman.generate_schedule_suggestions(
            student_data,
            available_time,
            subjects
        )
        return {"schedules": schedules}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggest-method")
async def suggest_study_method(
    subject: str,
    performance_data: Dict,
    available_minutes: int,
    current_user: User = Depends(get_current_user)
):
    """Suggest best study method for specific subject and time slot"""
    try:
        suggestion = await tman.suggest_study_method(
            subject,
            performance_data,
            available_minutes
        )
        return suggestion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-pattern")
async def analyze_study_pattern(
    performance_data: Dict,
    study_history: List[Dict],
    current_user: User = Depends(get_current_user)
):
    """Analyze study patterns and provide insights"""
    try:
        analysis = await tman.analyze_study_pattern(
            performance_data,
            study_history
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/methods")
async def get_study_methods():
    """Get all available study methods with descriptions"""
    return tman.study_methods

@router.post("/optimize-session")
async def optimize_study_session(
    subject: str,
    duration_minutes: int,
    energy_level: int,  # 1-5 scale
    current_user: User = Depends(get_current_user)
):
    """Get optimized study session plan"""
    try:
        # We'll implement this method in TmanAI
        session_plan = await tman.optimize_study_session(
            subject,
            duration_minutes,
            energy_level
        )
        return session_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
