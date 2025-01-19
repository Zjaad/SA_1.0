from datetime import datetime, timedelta

def test_create_schedule(client, auth_headers):
    # First, check available routes
    routes_response = client.get("/debug/routes")
    print("\nAvailable routes:", routes_response.json())

    schedule_data = {
        "name": "Test Schedule",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "preferences": {"preferred_time": "morning"},
        "user_id": 1
    }
    
    print("\nSending request with data:", schedule_data)
    print("Headers:", auth_headers)
    
    response = client.post("/schedules", json=schedule_data, headers=auth_headers)
    print("\nResponse status:", response.status_code)
    print("Response content:", response.content)
    
    assert response.status_code == 200

def test_get_schedule(client, auth_headers):
    # First create a schedule
    schedule_data = {
        "name": "Test Schedule",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "preferences": {"preferred_time": "morning"},
        "user_id": 1
    }
    create_response = client.post("/schedules", json=schedule_data, headers=auth_headers)
    schedule_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/schedules/{schedule_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == schedule_data["name"]

def test_update_schedule(client, auth_headers):
    # First create a schedule
    schedule_data = {
        "name": "Test Schedule",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "preferences": {"preferred_time": "morning"},
        "user_id": 1
    }
    create_response = client.post("/schedules", json=schedule_data, headers=auth_headers)
    schedule_id = create_response.json()["id"]

    # Update it
    update_data = {"name": "Updated Schedule"}
    response = client.put(f"/schedules/{schedule_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Schedule"
