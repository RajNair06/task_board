from fastapi import APIRouter,Depends,HTTPException,status
from db.models import User,Board,Card
from schemas.card_schemas import CardCreate,CardOut,CardUpdate,DeleteCardResponse
from task_board.utils.auth_utils import get_current_user,get_db
from sqlalchemy.orm import Session
router=APIRouter(tags=["cards"])

@router.post("/boards/{id}/cards",response_model=CardOut)
def create_card(id:int,card_data:CardCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    board=(db.query(Board).filter(Board.id==id,Board.created_by==current_user.id).first())
    if board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    card=Card(
        title=card_data.title,description=card_data.description,board_id=board.id,position=card_data.position,created_by=current_user.id
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card
 
@router.get("/boards/{id}/cards")
def get_cards(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    cards=(db.query(Card).filter(Card.board_id==id,Card.created_by==current_user.id).order_by(Card.position).all())
    if cards is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    return cards

@router.get("/boards/{board_id}/cards/{card_id}",response_model=CardOut)
def get_card_by_id(board_id:int,card_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    card=(db.query(Card).filter(Card.board_id==board_id,Card.id==card_id,Card.created_by==current_user.id).order_by(Card.position).first())
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    return card

@router.patch("/boards/{board_id}/cards/{card_id}",response_model=CardOut)
def update_card(board_id:int,card_id:int,card_data:CardUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    card=(db.query(Card).filter(Card.board_id==board_id,Card.id==card_id,Card.created_by==current_user.id).order_by(Card.position).first())
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    if card_data.title:
        card.title=card_data.title
    if card_data.description:
        card.description=card_data.description
    if card_data.position:
        card.position=card_data.position
    
    db.commit()
    return card


@router.delete("/boards/{board_id}/cards/{card_id}")
def delete_card(board_id:int,card_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    card=(db.query(Card).filter(Card.board_id==board_id,Card.id==card_id,Card.created_by==current_user.id).order_by(Card.position).first())
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    db.delete(card)
    db.commit()
    return DeleteCardResponse(
        name=card.title,
        message=f"Card with title'{card.title}' deleted successfully!"
    )


    
    


