from fastapi import APIRouter,Depends,HTTPException,status
from db.models import User,Board,Card
from commands.cards import CreateCardCommand,UpdateCardCommand,DeleteCardCommand
from queries.cards import GetCardQuery,ListCardQuery
from queries.handlers import CardQueryHandler
from commands.handlers import CardCommandHandler
from schemas.card_schemas import CardCreate,CardOut,CardUpdate,DeleteCardResponse
from utils.auth_utils import get_current_user,get_db
from sqlalchemy.orm import Session
router=APIRouter(tags=["cards"])

@router.post("/boards/{id}/cards",response_model=CardOut)
def create_card(id:int,card_data:CardCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    command=CreateCardCommand(board_id=id,user_id=current_user.id,position=card_data.position,title=card_data.title,description=card_data.description)
    return CardCommandHandler(db).handle(command)
 
@router.get("/boards/{id}/cards")
def get_cards(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    query=ListCardQuery(board_id=id,user_id=current_user.id)
    return CardQueryHandler(db).handle(query)


@router.get("/boards/{board_id}/cards/{card_id}",response_model=CardOut)
def get_card_by_id(board_id:int,card_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    query=GetCardQuery(id=card_id,board_id=board_id,user_id=current_user.id)
    return CardQueryHandler(db).handle(query)

@router.patch("/boards/{board_id}/cards/{card_id}",response_model=CardOut)
def update_card(board_id:int,card_id:int,card_data:CardUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    command=UpdateCardCommand(id=card_id,title=card_data.title,description=card_data.description,position=card_data.position,board_id=board_id,user_id=current_user.id)
    return CardCommandHandler(db).handle(command)
    


@router.delete("/boards/{board_id}/cards/{card_id}")
def delete_card(board_id:int,card_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    command=DeleteCardCommand(id=card_id,board_id=board_id,user_id=current_user.id)
    CardCommandHandler(db).handle(command)
    return {
        "message":"Card deleted successfully!"
    }


    
    


