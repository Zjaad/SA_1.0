import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def test_generate_schedule(client, auth_headers):
    # Test data
    student_data = {
        "education_level": "high_school",
        "preferred_study_time": "morning",
        "energy_peaks": ["09:00", "16:00"],
        "subject_preferences": {
            "math": 5,
            "physics": 4,
            "chemistry": 3
        }
    }
    
    available_time = {
        "monday": ["08:00-12:00", "14:00-18:00"],
        "tuesday": ["09:00-12:00", "15:00-19:00"],
        "wednesday": ["08:00-12:00", "14:00-18:00"],
        "thursday": ["09:00-12:00", "15:00-19:00"],
        "friday": ["08:00-12:00", "14:00-18:00"]
    }
    
    subjects = ["Mathematics", "Physics", "Chemistry"]

    response = client.post(
        "/tman/generate-schedule",
        json={
            "student_data": student_data,
            "available_time": available_time,
            "subjects": subjects
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "schedules" in data
    assert len(data["schedules"]) > 0

def test_suggest_study_method(client, auth_headers):
    test_data = {
        "subject": "Mathematics",
        "performance_data": {
            "recent_scores": [85, 78, 92],
            "difficult_topics": ["calculus", "trigonometry"],
            "preferred_methods": ["active_recall", "pomodoro"]
        },
        "available_minutes": 120
    }

    response = client.post(
        "/tman/suggest-method",
        json=test_data,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "method" in data
    assert "duration" in data
    assert "steps" in data

def test_analyze_pattern(client, auth_headers):
    performance_data = {
        "subjects": {
            "math": {"scores": [85, 90, 88], "study_hours": 20},
            "physics": {"scores": [75, 82, 80], "study_hours": 15}
        }
    }

    study_history = [
        {
            "date": datetime.now().isoformat(),
            "subject": "math",
            "duration": 120,
            "method": "pomodoro",
            "effectiveness": 4
        },
        {
            "date": (datetime.now() - timedelta(days=1)).isoformat(),
            "subject": "physics",
            "duration": 90,
            "method": "feynman",
            "effectiveness": 5
        }
    ]

    response = client.post(
        "/tman/analyze-pattern",
        json={
            "performance_data": performance_data,
            "study_history": study_history
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "best_time_slots" in data
    assert "effective_methods" in data

def test_get_study_methods(client):
    response = client.get("/tman/methods")
    
    assert response.status_code == 200
    methods = response.json()
    assert "pomodoro" in methods
    assert "spaced_repetition" in methods
    assert "active_recall" in methods
    assert "80_20" in methods

def test_optimize_session(client, auth_headers):
    test_data = {
        "subject": "Physics",
        "duration_minutes": 120,
        "energy_level": 4
    }

    response = client.post(
        "/tman/optimize-session",
        json=test_data,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "method" in data
    assert "duration" in data
    assert "steps" in data
    assert "materials_needed" in data
