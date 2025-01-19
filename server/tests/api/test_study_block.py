from datetime import datetime, timedelta

def test_create_study_block(client, auth_headers):
    # First create a schedule
    schedule_data = {
        "name": "Test Schedule",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "preferences": {"preferred_time": "morning"},
        "user_id": 1
    }
    schedule_response = client.post("/schedules", json=schedule_data, headers=auth_headers)
    schedule_id = schedule_response.json()["id"]

    # Create study block
    block_data = {
        "schedule_id": schedule_id,
        "subject_id": 1,
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "priority": 1
    }
    response = client.post("/study-blocks", json=block_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["schedule_id"] == schedule_id

def test_complete_study_block(client, auth_headers):
    # Create schedule and study block first
    schedule_data = {
        "name": "Test Schedule",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "preferences": {"preferred_time": "morning"},
        "user_id": 1
    }
    schedule_response = client.post("/schedules", json=schedule_data, headers=auth_headers)
    schedule_id = schedule_response.json()["id"]

    block_data = {
        "schedule_id": schedule_id,
        "subject_id": 1,
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "priority": 1
    }
    block_response = client.post("/study-blocks", json=block_data, headers=auth_headers)
    block_id = block_response.json()["id"]

    # Complete the study block
    response = client.post(f"/study-blocks/{block_id}/complete?efficiency_rating=5", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["is_completed"] == True
