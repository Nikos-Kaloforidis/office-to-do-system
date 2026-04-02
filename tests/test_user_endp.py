from app.models.user import User as UserModel
from app.models.user import Department as DepartmentModel
from .utils import login_user


def test_show_all_users(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    user1 = UserModel(username="u1", password="p", firstName="A", lastName="B")
    user2 = UserModel(username="u2", password="p", firstName="C", lastName="D")
    db_session.add_all([user1, user2])
    db_session.commit()

    response = client.get("api/users/show/all", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) >= 2


def test_show_user_by_id(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    new_user = UserModel(
        username="find_me", password="p", firstName="John", lastName="Doe"
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    response = client.get(f"api/users/show/{new_user.user_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["username"] == "find_me"


def test_show_user_not_found(client):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("api/users/show/9999", headers=headers)
    assert response.status_code == 404


def test_create_user(client):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "username": "new_user_api",
        "password": "securepassword",
        "firstName": "New",
        "lastName": "User",
    }
    response = client.post("api/users/create", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json()["username"] == "new_user_api"


def test_delete_user(client, db_session):
    user_to_del = UserModel(
        username="delete_me", password="pass", firstName="D", lastName="E"
    )
    db_session.add(user_to_del)
    db_session.commit()

    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}
    # 4. Action: Call the API
    response = client.delete(f"api/users/remove/{user_to_del.user_id}", headers=headers)

    # 5. Assertions
    assert response.status_code == 204

    # 6. Verify: Query again using the ID, not the old object
    check = (
        db_session.query(UserModel)
        .filter(UserModel.user_id == user_to_del.user_id)
        .first()
    )
    assert check is None


def test_update_user_password(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    user = UserModel(
        username="pass_update", password="old", firstName="P", lastName="U"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    payload = {"id": user.user_id, "password": "newpassword123"}
    response = client.put(
        f"api/users/update/password/{user.user_id}", json=payload, headers=headers
    )

    assert response.status_code == 200
    assert response.json()["username"] == "pass_update"


def test_update_user_department(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    dep = DepartmentModel(name="NewDept", domain="Domain")
    user = UserModel(username="dept_change", password="p", firstName="F", lastName="L")
    db_session.add_all([dep, user])
    db_session.commit()
    db_session.refresh(dep)
    db_session.refresh(user)

    response = client.put(
        f"api/users/update/department/{user.user_id}/{dep.dep_id}", headers=headers
    )

    assert response.status_code == 200
    assert response.json()["dep_id"] == dep.dep_id


def test_get_my_info(client):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("api/users/me", headers=headers)

    assert response.status_code == 200
    assert "username" in response.json()
