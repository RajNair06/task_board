from routers.auth import get_current_user
from schemas.boards_schemas import BoardCreate,BoardOut
from sqlalchemy.orm import Session
from db.models import User,Board
from utils.auth_utils import get_current_user,get_db
from fastapi import APIRouter,Depends,HTTPException

router=APIRouter(tags=["boardfroms"])

@router.post('/boards',response_model=BoardOut)
def create_board(board_data:BoardCreate,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    board=Board(name=board_data.name,description=board_data.description,created_by=current_user.id)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


@router.get("/boards/{id}",response_model=BoardOut)
def get_board(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    board=(db.query(Board).filter(Board.id==id,Board.created_by==current_user.id).first())
    if board is None:
        raise HTTPException(status_code=404,detail="board not found ")
    return board







