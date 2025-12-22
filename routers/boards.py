from routers.auth import get_current_user
from schemas.boards_schemas import BoardCreate,BoardOut,BoardUpdate,DeleteBoardResponse
from commands.boards import CreateBoardCommand,UpdateBoardCommand,DeleteBoardCommand
from queries.boards import GetBoardQuery,ListBoardsQuery
from queries.handlers import BoardQueryHandler
from commands.handlers import BoardCommandHandler
from sqlalchemy.orm import Session
from db.models import User,Board
from utils.auth_utils import get_current_user,get_db
from fastapi import APIRouter,Depends,HTTPException

router=APIRouter(tags=["boards"])

@router.post('/boards',response_model=BoardOut)
def create_board(board_data:BoardCreate,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    command=CreateBoardCommand(name=board_data.name,description=board_data.description,user_id=current_user.id)
    return BoardCommandHandler(db).handle(command)


@router.get("/boards/{id}",response_model=BoardOut)
def get_board(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    query=GetBoardQuery(id,current_user.id)
    return BoardQueryHandler(db).handle(query)

@router.get("/boards")
def list_boards(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    query=ListBoardsQuery(current_user.id)
    return BoardQueryHandler(db).handle(query)

@router.patch("/boards/{id}",response_model=BoardOut)
def update_board(id:int,board_update:BoardUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    command=UpdateBoardCommand(name=board_update.name,description=board_update.description,user_id=current_user.id,board_id=id)
    return BoardCommandHandler(db).handle(command)

@router.delete("/boards/{id}")
def delete_board(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    command=DeleteBoardCommand(board_id=id,user_id=current_user.id)
    BoardCommandHandler(db).handle(command)
    return {"message": "Board deleted successfully"}
    
    
    







