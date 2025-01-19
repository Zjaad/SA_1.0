import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, get_db
from src.main import app

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_user(client):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",  # This matches what we use in auth_headers
        "password": "test123",
        "full_name": "Test User",
        "country": "Morocco",
        "education_level": "High School",
        "specialization": "Science"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def auth_headers(client, test_user):
    response = client.post("/auth/token", data={
        "username": "testuser",  # This now matches the registered username
        "password": "test123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(autouse=True)
def verify_db(db_session):
    # Print all tables in the database
    from sqlalchemy import inspect
    inspector = inspect(db_session.bind)
    print("\nAvailable tables:", inspector.get_table_names())
    yield
    
@pytest.fixture
def tman_test_user(client):
    user_data = {
        "email": "tman_test@example.com",
        "username": "tman_tester",
        "password": "test123",
        "full_name": "Test User",
        "country": "Morocco",
        "education_level": "High School",
        "specialization": "Science"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def tman_auth_headers(client, tman_test_user):
    response = client.post("/auth/token", data={
        "username": "tman_tester",
        "password": "test123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
