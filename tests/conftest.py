from task_board.main import app
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import os
from db.models import *
from routers.auth import get_db
import pytest
import tempfile

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
    engine=create_engine(url)
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

@pytest.fixture
def client(db_session):
    def override_get_db():
        
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db]=override_get_db

    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.pop(get_db,None)

