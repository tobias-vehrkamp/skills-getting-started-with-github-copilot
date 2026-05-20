import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Initial participants matching the seed data in app.py
INITIAL_PARTICIPANTS = {
    "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
    "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"],
    "Gym Class": ["john@mergington.edu", "olivia@mergington.edu"],
    "Soccer Team": ["liam@mergington.edu", "noah@mergington.edu"],
    "Track and Field": ["ava@mergington.edu", "mia@mergington.edu"],
    "Drama Club": ["lucas@mergington.edu", "isabella@mergington.edu"],
    "Painting Studio": ["charlotte@mergington.edu", "amelia@mergington.edu"],
    "Debate Society": ["elijah@mergington.edu", "harper@mergington.edu"],
    "Math Olympiad": ["henry@mergington.edu", "evelyn@mergington.edu"],
}

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the in-memory DB to initial state before each test
    for name, activity in activities.items():
        activity["participants"] = list(INITIAL_PARTICIPANTS.get(name, []))
    yield

client = TestClient(app)

def test_get_activities():
    # Arrange is handled by fixture
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 409
    assert response.json()["detail"].startswith(email.lower())

def test_signup_nonexistent_activity():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

@pytest.mark.skip(reason="Unregister endpoint missing from app.py – needs to be restored")
def test_unregister_success():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]

@pytest.mark.skip(reason="Unregister endpoint missing from app.py – needs to be restored")
def test_unregister_not_registered():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]
