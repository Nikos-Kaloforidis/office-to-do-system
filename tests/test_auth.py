import os
from .utils import populate_db, get_test_user
from jose import jwt


def test_login_success(client, db_session):

    populate_db(db_session)
    test_user = get_test_user(db_session)
    login_data = {"username": "testUser", "password": "testpassword123"}
    response = client.post("/authenticate/", json=login_data)

    assert response.status_code == 202
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user_id"] == test_user.user_id
    assert data["username"] == test_user.username

    secret_key = os.getenv("SECRET_KEY")
    payload = jwt.decode(data["access_token"], secret_key, algorithms=["HS256"])
    assert payload["sub"] == test_user.username
    assert payload["user_id"] == test_user.user_id


def test_login_invalid_credentials(client, db_session):

    response = client.post(
        "/authenticate/", json={"username": "testUser", "password": "not_the_password"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_get_current_user_dependency(client, db_session):
    test_user = get_test_user(db_session)

    login_res = client.post(
        "/authenticate/",
        json={"username": test_user.username, "password": "testpassword123"},
    )
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/api/users/show/{test_user.user_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["username"] == test_user.username


def test_expired_or_invalid_token(client):
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.get("/api/users/show/1", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
