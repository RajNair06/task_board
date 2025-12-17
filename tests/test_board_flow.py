import pytest
from fastapi import HTTPException
from db.models import Board

def test_create_board(client,db_session,user_setup):
    token=user_setup
    
    payload={
        "name":"Test Board",
        "description":"Sample "
    }
    response=client.post("/boards", headers={"Authorization": f"Bearer {token}"},json=payload)
    assert response.status_code==200
    response=response.json()
    
    db_session.commit()
    board=db_session.query(Board).filter_by(id=response["id"]).first()
    assert board is not None, "Board should exist in database after creation"
    assert board.name == payload["name"]
    assert board.description == payload["description"]

def test_update_board(client, db_session, user_setup):
    token = user_setup

    
    create_payload = {
        "name": "Original Board",
        "description": "Original Description"
    }

    create_response = client.post(
        "/boards",
        headers={"Authorization": f"Bearer {token}"},
        json=create_payload
    )

    assert create_response.status_code == 200
    created_board = create_response.json()
    board_id = created_board["id"]

    
    update_payload = {
        "name": "New Board Name",
        "description": "New Sample Description"
    }

    update_response = client.patch(
        f"/boards/{board_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_payload
    )

    assert update_response.status_code == 200
    updated_board = update_response.json()

    
    assert updated_board["name"] == update_payload["name"]
    assert updated_board["description"] == update_payload["description"]

    
    board = db_session.get(Board, board_id)
    assert board is not None, "Board should exist in database after update"
    assert board.name == update_payload["name"]
    assert board.description == update_payload["description"]


def test_delete_board(client, db_session, user_setup):
    token = user_setup

    
    create_payload = {
        "name": "Board To Delete",
        "description": "Temporary board"
    }

    create_response = client.post(
        "/boards",
        headers={"Authorization": f"Bearer {token}"},
        json=create_payload
    )

    assert create_response.status_code == 200
    created_board = create_response.json()
    board_id = created_board["id"]

    
    delete_response = client.delete(
        f"/boards/{board_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert delete_response.status_code == 200
    delete_body = delete_response.json()

    
    assert delete_body["name"] == create_payload["name"]
    assert "deleted successfully" in delete_body["message"]

   
    board = db_session.get(Board, board_id)
    assert board is None, "Board should be removed from database"
