"""Security tests for authentication, authorization, and data isolation."""
from tests.conftest import login, auth


def test_protected_route_rejects_no_token(client):
    res = client.get("/notes")
    assert res.status_code == 401


def test_protected_route_rejects_bad_token(client):
    result = client.get("/notes", headers=auth("not.a.jwt"))
    assert result.status_code == 401


def test_user_cannot_read_another_users_note(client):
    token = login(client, "alice", "alicepass")
    assert token
    result = client.get("/notes/2", headers=auth(token))
    assert result.status_code == 403


def test_user_can_read_own_note(client):
    token = login(client, "alice", "alicepass")
    assert token
    result = client.get("/notes/1", headers=auth(token))
    assert result.status_code == 200
    assert result.json()["owner_id"] == 2


def test_login_does_not_reveal_which_field_was_wrong(client):
    unknown_user = client.post(
        "/login", json={"username": "unknown", "password": "alicepass"}
    )
    wrong_password = client.post(
        "/login", json={"username": "alice", "password": "wrongpass"}
    )
    assert unknown_user.status_code == 401
    assert wrong_password.status_code == 401
    assert unknown_user.json() == wrong_password.json()


def test_non_admin_cannot_list_users(client):
    token = login(client, "alice", "alicepass")
    assert token
    result = client.get("/admin/users", headers=auth(token))
    assert result.status_code == 403


def test_admin_can_list_users_without_password_leak(client):
    token = login(client, "admin", "admin123")
    assert token
    result = client.get("/admin/users", headers=auth(token))
    assert result.status_code == 200
    assert result.json()
    for user in result.json():
        assert set(user) == {"id", "username", "is_admin"}
        assert "password" not in user
