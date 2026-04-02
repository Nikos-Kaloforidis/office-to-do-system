from app.models.user import User as UserModel
from app.models.user import Department as DepartmentModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def login_user(client):
    login_data = {"username": "testUser", "password": "testpassword123"}
    response = client.post("/authenticate/", json=login_data)
    data = response.json()
    return data["access_token"]


def populate_db(db_session):

    raw_password = "testpassword123"
    hashed_password = pwd_context.hash(raw_password)
    test_user = UserModel(
        username="testUser",
        password=hashed_password,
        firstName="John",
        lastName="Doe",
        dep_id=1,
    )
    test_department = DepartmentModel(name="TestDep", domain="TestDomain")

    db_session.add(test_department)
    db_session.add(test_user)
    db_session.commit()


def get_test_user(db_session):
    return db_session.query(UserModel).filter(UserModel.username == "testUser").first()


def get_test_department(db_session):
    return (
        db_session.query(DepartmentModel)
        .filter(DepartmentModel.name == "TestDep")
        .first()
    )
