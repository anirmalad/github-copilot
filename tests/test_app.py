import copy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

import src.app as app_module

client = TestClient(app_module.app)
BASE_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(BASE_ACTIVITIES))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(BASE_ACTIVITIES))


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity():
    email = "test.student@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_fails():
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already registered for this activity"


def test_unregister_from_activity():
    email = "daniel@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{quote(activity_name)}/unregister?email={quote(email)}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_not_registered_fails():
    email = "unknown@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{quote(activity_name)}/unregister?email={quote(email)}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_activity_not_found_for_signup():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_activity_not_found_for_unregister():
    response = client.post("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in {307, 308}
    assert response.headers["location"] == "/static/index.html"
