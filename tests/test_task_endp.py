import pytest
from app.models.user import User as UserModel
from app.models.task import Task as TaskModel
from .utils import login_user


def test_create_task(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    user = db_session.query(UserModel).first()

    payload = {
        "name": "Finish Report",
        "description": "Quarterly analysis",
        "status": "requested",
        "created_by_id": user.user_id,
        "assigned_user_id": user.user_id,
    }

    response = client.post("api/tasks/", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json()["name"] == "Finish Report"


def test_read_all_tasks(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    user = db_session.query(UserModel).first()
    task = TaskModel(name="Task 1", created_by_id=user.user_id)
    db_session.add(task)
    db_session.commit()

    response = client.get("api/tasks/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["tasks"]) >= 1


def test_read_task_by_id(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    user = db_session.query(UserModel).first()
    new_task = TaskModel(name="Specific Task", created_by_id=user.user_id)
    db_session.add(new_task)
    db_session.commit()
    db_session.refresh(new_task)

    response = client.get(f"api/tasks/{new_task.task_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Specific Task"


def test_update_task_status(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    user = db_session.query(UserModel).first()
    task = TaskModel(name="Old Status", created_by_id=user.user_id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    payload = {"status": "working"}
    response = client.patch(f"api/tasks/{task.task_id}", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["status"] == "working"


def test_delete_task(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    user = db_session.query(UserModel).first()
    task_to_del = TaskModel(name="To be deleted", created_by_id=user.user_id)
    db_session.add(task_to_del)
    db_session.commit()
    db_session.refresh(task_to_del)

    t_id = task_to_del.task_id

    response = client.delete(f"api/tasks/{t_id}", headers=headers)

    assert response.status_code == 204
    check = db_session.query(TaskModel).filter_by(task_id=t_id).first()
    assert check is None


def test_get_tasks_by_user(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    user = db_session.query(UserModel).first()
    task = TaskModel(
        name="User Task", created_by_id=user.user_id, assigned_user_id=user.user_id
    )
    db_session.add(task)
    db_session.commit()

    response = client.get(f"api/tasks/user/{user.user_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_get_tasks_by_department(client, db_session):
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    user = db_session.query(UserModel).first()
    task = TaskModel(name="Dept Task", created_by_id=user.user_id, assigned_dep_id=1)
    db_session.add(task)
    db_session.commit()

    response = client.get(f"api/tasks/department/{user.dep_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["total"] >= 1
