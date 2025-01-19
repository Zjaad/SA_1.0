from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from datetime import datetime

from src.database import get_db
from src.services.ai_integration import TmanAI
from src.services.auth import get_current_user
from src.models.user import User

router = APIRouter(prefix="/tman", tags=["ai-features"])

# Initialize TmanAI
tman_ai = TmanAI()


@router.post("/analyze-patterns", response_model=PatternAnalysisResponse)
async def analyze_patterns(
    request: PatternAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze user's study patterns and provide insights"""
    try:
        analysis = await tman_ai.analyze_study_pattern(
            user_data={
                "education_level": current_user.education_level,
                "specialization": current_user.specialization
            },
            study_history=request.study_history
        )
        return PatternAnalysisResponse(**analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize-schedule", response_model=OptimizedSchedule)
async def optimize_schedule(
    request: ScheduleOptimizationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI-optimized schedule"""
    try:
        return await tman_ai.optimize_schedule(
            request.schedule_data,
            request.performance_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest-method", response_model=StudyMethodSuggestion)
async def suggest_study_method(
    request: StudyMethodRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-suggested study method"""
    try:
        return await tman_ai.suggest_study_method(
            request.subject,
            request.topic,
            request.context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/smart-break", response_model=SmartBreakSuggestion)
async def suggest_break(
    request: SmartBreakRequest,
    current_user: User = Depends(get_current_user)
):
    """Get AI-suggested break timing and activity"""
    try:
        suggestion = await tman_ai.suggest_break({
            "study_duration": request.study_duration,
            "energy_level": request.energy_level,
            "last_break": request.last_break,
            "user_level": current_user.education_level
        })
        return SmartBreakSuggestion(**suggestion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
