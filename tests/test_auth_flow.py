import pytest
from utils.auth_utils import get_password_hash,create_access_token
from datetime import timedelta
from db.models import User


def test_register_and_login_json(client,db_session):
    payload={"email": "alice@example.com", "password": "hunter2","name":"Alice"}
    response=client.post("/auth/register",json=payload)
    assert response.status_code==201
    data=response.json()
    assert data["email"]=="alice@example.com"
    assert "id" in data
    login_payload={"email": "alice@example.com", "password": "hunter2"}
    response=client.post("/auth/token_json",json=login_payload)
    token=response.json()
    assert "access_token"  in token and token["token_type"]=="Bearer"

    headers={"Authorization":f"Bearer {token["access_token"]}"}
    response=client.get("/auth/me",headers=headers)
    assert response.status_code==200
    self_user=response.json()
    assert self_user["email"]=="alice@example.com"

def test_login_form_and_protected(client,db_session):
    hashed=get_password_hash("secretpw")
    user=User(email="bob@example.com",password_hash=hashed,name="Bob")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response=client.post("/auth/token",data={"username": "bob@example.com", "password": "secretpw"})
    assert response.status_code==200
    token=response.json()["access_token"]
    response = client.get("/auth/me", headers={
        "Content-Type": "application/json","Authorization": f"Bearer {token}"
        })
    assert response.status_code == 200
    assert response.json()["email"] == "bob@example.com"

def test_bad_credentials(client):
    response=client.post("auth/token_json",json={"email":"no@user.com","password":"x"})
    assert response.status_code==401

def test_missing_token_protected(client):
    r = client.get("/auth/me")
    
    assert r.status_code == 401


def test_expired_token(client,db_session):
    from utils.auth_utils import ACCESS_TOKEN_EXPIRY_DURATION
    hashed=get_password_hash("pw")
    user = User(email="expired@example.com", password_hash=hashed,name="rando")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    token = create_access_token(user.id,timedelta(seconds=-10))
    
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401






