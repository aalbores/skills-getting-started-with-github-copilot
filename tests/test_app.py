import uuid

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_registers_participant_for_activity():
    # Arrange
    activity_name = "Soccer Club"
    email = f"signup-{uuid.uuid4().hex}@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = f"duplicate-{uuid.uuid4().hex}@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_removes_participant():
    # Arrange
    activity_name = "Track and Field"
    email = f"remove-{uuid.uuid4().hex}@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
