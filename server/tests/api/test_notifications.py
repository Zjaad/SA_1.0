from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient

def test_schedule_study_notifications(client, auth_headers):
    # Test data
    study_data = {
        "subject": "Mathematics",
        "topic": "Calculus - Derivatives",
        "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "duration": 60
    }

    response = client.post(
        "/notifications/schedule-study",
        json=study_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    notifications = data["notifications"]
    
    # Check if we got the right notifications
    assert len(notifications) > 0
    # Check study start notification
    start_notif = notifications[0]
    assert "Mathematics" in start_notif["title"]
    assert "Calculus" in start_notif["message"]

def test_schedule_exam_notifications(client, auth_headers):
    exam_data = {
        "subject": "Physics",
        "exam_date": (datetime.now() + timedelta(days=7)).isoformat()
    }

    response = client.post(
        "/notifications/schedule-exam",
        json=exam_data,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    notifications = data["notifications"]
    
    # Should have multiple reminders
    assert len(notifications) > 0
    # Check exam reminder content
    assert "Physics" in notifications[0]["title"]
    assert "exam" in notifications[0]["message"].lower()

def test_schedule_review_notifications(client, auth_headers):
    review_data = {
        "subject": "Chemistry",
        "topic": "Periodic Table",
        "study_date": datetime.now().isoformat()
    }

    response = client.post(
        "/notifications/schedule-review",
        json=review_data,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    notifications = data["notifications"]
    
    # Should create multiple review reminders
    assert len(notifications) > 0
    # Check review reminder content
    assert "Chemistry" in notifications[0]["title"]
    assert "Periodic Table" in notifications[0]["message"]

def test_invalid_schedule_time(client, auth_headers):
    # Test with past time
    study_data = {
        "subject": "Biology",
        "topic": "Cell Structure",
        "start_time": (datetime.now() - timedelta(hours=1)).isoformat(),
        "duration": 30
    }

    response = client.post(
        "/notifications/schedule-study",
        json=study_data,
        headers=auth_headers
    )
    
    # Should return error for past time
    assert response.status_code == 400

def test_notification_formatting(client, auth_headers):
    study_data = {
        "subject": "French",
        "topic": "Grammar",
        "start_time": (datetime.now() + timedelta(minutes=30)).isoformat(),
        "duration": 45
    }

    response = client.post(
        "/notifications/schedule-study",
        json=study_data,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    notification = data["notifications"][0]
    
    # Check notification structure
    assert "title" in notification
    assert "message" in notification
    assert "schedule_time" in notification
    assert "type" in notification
