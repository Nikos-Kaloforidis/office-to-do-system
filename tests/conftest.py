import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db  # Import your real Base and get_db
from app.main import app  # Import your FastAPI app
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os

load_dotenv
# 1. Point to the TEST database port (5433)
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# 2. Create a separate engine for testing
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create the tables in the test database once per test session."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    """Provides a fresh database session for a single test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """
    Overwrites the 'get_db' dependency in your FastAPI app
    to use the test database instead of the real one.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Clean up overrides after test
    app.dependency_overrides.clear()
