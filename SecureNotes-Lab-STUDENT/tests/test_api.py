"""API behaviour tests.

ONE example is written for you. Replace each `assert False` TODO with a real test.
Use the helpers from conftest:  login(client, user, pw) -> token,  auth(token) -> header.
Ask for the `client` fixture by adding it as a parameter (it gives you a fresh DB each time).

Run the suite:   pytest -q
Run one file:    pytest tests/test_api.py -q
"""
from tests.conftest import login, auth


# ----- EXAMPLE (already done) ---------------------------------------------
def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


# ----- TODO 1 -------------------------------------------------------------
def test_register_then_login(client):
    # Register a new user, then log in as that user.
    # Assert login returns 200 AND the access_token looks like a JWT
    # (three dot-separated parts: token.count(".") == 2).
    register = client.post(
        "/register", json={"username": "newuser", "password": "newpass"}
    )
    assert register.status_code == 200

    result = client.post(
        "/login", json={"username": "newuser", "password": "newpass"}
    )
    assert result.status_code == 200
    assert result.json()["access_token"].count(".") == 2


# ----- TODO 2 -------------------------------------------------------------
def test_login_wrong_password_is_401(client):
    # Log in as 'alice' with the WRONG password. Assert the status code is 401.
    result = client.post(
        "/login", json={"username": "alice", "password": "wrongpass"}
    )
    assert result.status_code == 401


# ----- TODO 3 -------------------------------------------------------------
def test_create_then_list_own_note(client):
    # Log in as alice, POST a new note, then GET /notes and assert the new
    # note's title appears in the list.
    token = login(client, "alice", "alicepass")
    create = client.post(
        "/notes",
        json={"title": "New note", "body": "New note body"},
        headers=auth(token),
    )
    assert create.status_code == 200

    notes = client.get("/notes", headers=auth(token))
    assert notes.status_code == 200
    assert any(note["title"] == "New note" for note in notes.json())
