from fastapi.testclient import TestClient
from main import app, reset_data

client = TestClient(app)



# 1. Health Check
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# 2. Create Task (Success)
def test_create_task():
    reset_data()

    payload = {
        "title": "Test Task",
        "description": "Testing",
        "status": "pending"
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Task"


# 3. Invalid Status (Validation Error)
def test_create_task_invalid_status():
    reset_data()

    payload = {
        "title": "Bad Task",
        "description": "Testing",
        "status": "wrong_status"
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422  # validation error


# 4. Get Tasks
def test_get_tasks():
    reset_data()

    client.post("/tasks", json={
        "title": "Task1",
        "description": "Test",
        "status": "pending"
    })

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


# 5. Task Not Found (Custom Exception)
def test_get_task_not_found():
    reset_data()

    response = client.get("/tasks/999")

    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "TaskNotFoundError"


# 6. Update Task
def test_update_task():
    reset_data()

    client.post("/tasks", json={
        "title": "Old",
        "description": "Old Desc",
        "status": "pending"
    })

    response = client.put("/tasks/1", json={
        "status": "completed"
    })

    assert response.status_code == 200
    assert response.json()["status"] == "completed"


# 7. Delete Task
def test_delete_task():
    reset_data()

    client.post("/tasks", json={
        "title": "To Delete",
        "description": "Test",
        "status": "pending"
    })

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"