from main import app
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import os
from db.models import *

from utils.auth_utils import get_password_hash,get_db
import pytest
import tempfile
from unittest.mock import patch, MagicMock
from contextlib import asynccontextmanager
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
    """Clean database before each test."""
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()

@pytest.fixture(autouse=True)
def mock_celery_tasks(db_session):
    """Mock Celery tasks to run synchronously for testing."""
    from tasks import process, log
    import db.database
    original = db.database.SessionLocal
    db.database.SessionLocal = lambda: db_session
    # Also patch in the task modules
    process.SessionLocal = lambda: db_session
    log.SessionLocal = lambda: db_session
    try:
        with patch.object(process.record_activity, 'delay') as mock_record, \
             patch.object(log.log_audit, 'delay') as mock_log:
            # Make delay return a mock that calls the function synchronously
            def sync_record(*args, **kwargs):
                process.record_activity(*args, **kwargs)
                return MagicMock()
            
            def sync_log(*args, **kwargs):
                log.log_audit(*args, **kwargs)
                return MagicMock()
            
            mock_record.side_effect = sync_record
            mock_log.side_effect = sync_log
            yield mock_record, mock_log
    finally:
        db.database.SessionLocal = original

@pytest.fixture(autouse=True)
def mock_redis():
    """Mock Redis clients for testing."""
    with patch('redis.Redis') as mock_sync_redis, \
         patch('redis.asyncio.Redis') as mock_async_redis:
        mock_sync_instance = MagicMock()
        mock_async_instance = MagicMock()
        mock_sync_redis.return_value = mock_sync_instance
        mock_async_redis.from_url.return_value = mock_async_instance
        mock_async_instance.pubsub.return_value = MagicMock()
        yield mock_sync_instance, mock_async_instance

@pytest.fixture
def client(db_session):
    print("get_db id:", id(get_db))

    # Create a test app without lifespan to avoid starting background tasks
    from fastapi import FastAPI
    from routers.auth import router as auth_router
    from routers.boards import router as boards_router
    from routers.cards import router as cards_router
    from routers.sockets import router as ws_router

    test_app = FastAPI()
    test_app.include_router(auth_router)
    test_app.include_router(boards_router)
    test_app.include_router(cards_router)
    test_app.include_router(ws_router)

    def override_get_db():
        yield db_session

    test_app.dependency_overrides[get_db] = override_get_db

    with TestClient(test_app) as c:
        yield c

    test_app.dependency_overrides.clear()



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