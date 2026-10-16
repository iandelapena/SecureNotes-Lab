"""API behavior tests for the SecureNotes application."""
from tests.conftest import login, auth


def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


def test_register_then_login(client):
    register = client.post(
        "/register", json={"username": "newuser", "password": "newpass"}
    )
    assert register.status_code == 200

    result = client.post(
        "/login", json={"username": "newuser", "password": "newpass"}
    )
    assert result.status_code == 200
    assert result.json()["access_token"].count(".") == 2
    assert result.json()["token_type"] == "bearer"


def test_login_wrong_password_is_401(client):
    result = client.post(
        "/login", json={"username": "alice", "password": "wrongpass"}
    )
    assert result.status_code == 401
    assert result.json()["detail"] == "Invalid username or password"


def test_create_then_list_own_note(client):
    token = login(client, "alice", "alicepass")
    assert token

    create = client.post(
        "/notes",
        json={"title": "New note", "body": "New note body"},
        headers=auth(token),
    )
    assert create.status_code == 200
    assert create.json()["title"] == "New note"

    notes = client.get("/notes", headers=auth(token))
    assert notes.status_code == 200
    assert any(note["title"] == "New note" for note in notes.json())
