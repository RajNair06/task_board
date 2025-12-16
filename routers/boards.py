from routers.auth import get_current_user
from schemas.boards_schemas import BoardCreate,BoardOut,BoardUpdate,DeleteBoardResponse
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

@router.patch("/boards/{id}",response_model=BoardOut)
def update_board(id:int,board_update:BoardUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    board=(db.query(Board).filter_by(id=id,created_by=current_user.id).first())
    if board is None:
        raise HTTPException(status_code=404,detail="board not found ")
    if board_update.name:
        board.name=board_update.name
    if board_update.description:
        board.description=board_update.description

    return board

@router.delete("/boards/{id}")
def delete_board(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    board=(db.query(Board).filter_by(id=id,created_by=current_user.id).first())
    if board is None:
        raise HTTPException(status_code=404,detail="board not found ")
    db.delete(board)
    db.commit()
    return DeleteBoardResponse(
        name=board.name,
        message=f"Board '{board.name}' deleted successfully"

    )
    
    
    







