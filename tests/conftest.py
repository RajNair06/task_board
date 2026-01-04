from main import app
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import os
from db.models import *

from utils.auth_utils import get_password_hash,get_db
import pytest
import tempfile
print("get_db id:", id(get_db))


@pytest.fixture(scope="session")
def db_file():
    fd,path=tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    try:
        os.remove(path)
    except Exception as e:
        pass

@pytest.fixture(scope="session")
def test_engine(db_file):
    url=f"sqlite:///{db_file}"
    engine=create_engine(url,
    connect_args={"check_same_thread": False}
)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()

@pytest.fixture
def TestSessionLocal(test_engine):
    return sessionmaker(bind=test_engine)

@pytest.fixture
def db_session(TestSessionLocal):
    session=TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(autouse=True)
def clean_database(db_session):
    yield
    meta=Base.metadata
    for table in reversed(meta.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()

@pytest.fixture
def client(db_session):
    print("get_db id:", id(get_db))

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()



@pytest.fixture
def user_setup(client, db_session):
    user = db_session.query(User).filter_by(email="bob@example.com").first()

    if not user:
        hashed = get_password_hash("secretpw")
        user = User(
            email="bob@example.com",
            password_hash=hashed,
            name="Bob"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

    response = client.post(
        "/auth/token_json",
        json={"email": "bob@example.com", "password": "secretpw"}
    )

    assert response.status_code == 200
    token = response.json()["access_token"]
    return token

@pytest.fixture
def member_user_setup(client, db_session):
    user = db_session.query(User).filter_by(email="sarah@example.com").first()

    if not user:
        hashed = get_password_hash("secretpw")
        user = User(
            email="sarah@example.com",
            password_hash=hashed,
            name="Sarah"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

    response = client.post(
        "/auth/token_json",
        json={"email": "sarah@example.com", "password": "secretpw"}
    )


    assert response.status_code == 200
    
    user = db_session.query(User).filter_by(email="sarah@example.com").first()
    return user.id
@pytest.fixture
def other_user_setup(client, db_session):
    """Fixture for a third user to test non-member permissions."""
    user = db_session.query(User).filter_by(email="alice@example.com").first()

    if not user:
        hashed = get_password_hash("secretpw")
        user = User(
            email="alice@example.com",
            password_hash=hashed,
            name="Alice"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

    response = client.post(
        "/auth/token_json",
        json={"email": "alice@example.com", "password": "secretpw"}
    )

    assert response.status_code == 200
    
    user = db_session.query(User).filter_by(email="alice@example.com").first()
    return user.id