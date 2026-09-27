import pytest
from fastapi.testclient import TestClient
from app.main import app, tasks

pytestmark = pytest.mark.api

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    yield
    tasks.clear()

def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Learn QA Automation",
            "description": "Practice API testing"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Learn QA Automation"
    assert data["description"] == "Practice API testing"
    assert data["completed"] is False
    assert "id" in data

def test_create_task_without_description():
    response = client.post(
        "/tasks",
        json={
            "title": "Test task"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test task"
    assert data["description"] is None
    assert data["completed"] is False

def test_create_task_without_title():
    response = client.post(
        "/tasks",
        json={
            "description": "Task without title"
        }
    )

    assert response.status_code == 422

def test_create_task_invalid_completed():
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid task",
            "completed": "banana"
        }
    )

    assert response.status_code == 422



def test_get_tasks_returns_tasks():
    client.post(
        "/tasks",
        json={
            "title": "Task for GET"
        }
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to delete"
        }
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted successfully"

def test_delete_nonexistent_task():
    response = client.delete("/tasks/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

