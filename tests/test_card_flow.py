import pytest
from db.models import Board, Card
def test_create_card(client, db_session, user_setup):
    token = user_setup

    
    board_payload = {
        "name": "Board For Cards",
        "description": "Card container"
    }

    board_response = client.post(
        "/boards",
        headers={"Authorization": f"Bearer {token}"},
        json=board_payload
    )

    assert board_response.status_code == 200
    board = board_response.json()
    board_id = board["id"]

    
    card_payload = {
        "title": "Card 1",
        "description": "First card",
        "position": 1
    }

    card_response = client.post(
        f"/boards/{board_id}/cards",
        headers={"Authorization": f"Bearer {token}"},
        json=card_payload
    )

    assert card_response.status_code == 200
    card = card_response.json()

    
    db_card = db_session.get(Card, card["id"])
    assert db_card is not None
    assert db_card.title == card_payload["title"]
    assert db_card.description == card_payload["description"]
    assert db_card.position == card_payload["position"]
    assert db_card.board_id == board_id

def test_get_cards(client, db_session, user_setup):
    token = user_setup

    
    board_response = client.post(
        "/boards",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Order Board", "description": "Ordering test"}
    )
    board_id = board_response.json()["id"]

    
    cards = [
        {"title": "Card A", "description": "A", "position": 2},
        {"title": "Card B", "description": "B", "position": 1},
    ]

    for card in cards:
        client.post(
            f"/boards/{board_id}/cards",
            headers={"Authorization": f"Bearer {token}"},
            json=card
        )

    
    response = client.get(
        f"/boards/{board_id}/cards",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    result = response.json()

    assert len(result) == 2
    assert result[0]["position"] == 1
    assert result[1]["position"] == 2


def test_get_card_by_id(client, db_session, user_setup):
    token = user_setup

    
    board_id = client.post(
        "/boards",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Single Card Board", "description": ""}
    ).json()["id"]

    
    card = client.post(
        f"/boards/{board_id}/cards",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Solo Card", "description": "Only one", "position": 1}
    ).json()

    
    response = client.get(
        f"/boards/{board_id}/cards/{card['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    fetched = response.json()
    assert fetched["id"] == card["id"]


def test_update_card(client, db_session, user_setup):
    token = user_setup

    
    board_id = client.post(
        "/boards",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Update Card Board", "description": ""}
    ).json()["id"]

    
    card = client.post(
        f"/boards/{board_id}/cards",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Old Title", "description": "Old desc", "position": 1}
    ).json()

    
    update_payload = {
        "title": "New Title",
        "description": "New desc",
        "position": 2
    }

    response = client.patch(
        f"/boards/{board_id}/cards/{card['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_payload
    )

    assert response.status_code == 200
    updated = response.json()

    
    db_card = db_session.get(Card, card["id"])
    assert db_card.title == update_payload["title"]
    assert db_card.description == update_payload["description"]
    assert db_card.position == update_payload["position"]


def test_delete_card(client, db_session, user_setup):
    token = user_setup

    
    board_id = client.post(
        "/boards",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Delete Card Board", "description": ""}
    ).json()["id"]

    
    card = client.post(
        f"/boards/{board_id}/cards",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "To Delete", "description": "", "position": 1}
    ).json()

    
    response = client.delete(
        f"/boards/{board_id}/cards/{card['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    body = response.json()

    assert body["name"] == card["title"]
    assert "deleted successfully" in body["message"]

    
    db_card = db_session.get(Card, card["id"])
    assert db_card is None
