from app.models.user import Department as DepartmentModel
from app.models.user import User as UserModel
from .utils import login_user


def test_create_department(client):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"name": "Engineering", "domain": "Software Development"}
    response = client.post("api/department/add", json=payload, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Engineering"
    assert "dep_id" in data


def test_show_all_departments(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    dep1 = DepartmentModel(name="HR", domain="Human Resources")
    dep2 = DepartmentModel(name="Sales", domain="Retail")
    db_session.add_all([dep1, dep2])
    db_session.commit()

    response = client.get("api/department/show/all", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data["departments"]) >= 2
    assert any(d["name"] == "HR" for d in data["departments"])


def test_show_specific_department(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    new_dep = DepartmentModel(name="Legal", domain="Compliance")
    db_session.add(new_dep)
    db_session.commit()
    db_session.refresh(new_dep)

    response = client.get(f"api/department/show/{new_dep.dep_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Legal"


def test_show_department_not_found(client):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("api/department/show/9999", headers=headers)
    assert response.status_code == 404


def test_remove_department(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    dep_to_delete = DepartmentModel(name="Marketing", domain="Ads")
    db_session.add(dep_to_delete)
    db_session.commit()
    db_session.refresh(dep_to_delete)

    response = client.delete(
        f"api/department/remove/{dep_to_delete.dep_id}", headers=headers
    )

    assert response.status_code == 204
    check = (
        db_session.query(DepartmentModel).filter_by(dep_id=dep_to_delete.dep_id).first()
    )
    assert check is None


def test_get_all_users_from_department(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    dep = DepartmentModel(name="Tech", domain="IT")
    db_session.add(dep)
    db_session.commit()
    db_session.refresh(dep)

    user = UserModel(
        username="dept_user",
        password="password",
        firstName="Test",
        lastName="User",
        dep_id=dep.dep_id,
    )
    db_session.add(user)
    db_session.commit()

    response = client.get(f"api/department/all_users/{dep.dep_id}", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "dept_user"


def test_get_users_from_department_empty(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    empty_dep = DepartmentModel(name="Empty", domain="None")
    db_session.add(empty_dep)
    db_session.commit()
    db_session.refresh(empty_dep)

    response = client.get(
        f"api/department/all_users/{empty_dep.dep_id}", headers=headers
    )

    assert response.status_code == 404
