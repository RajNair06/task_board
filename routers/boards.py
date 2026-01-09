from routers.auth import get_current_user
from schemas.boards_schemas import BoardCreate,BoardOut,BoardUpdate,DeleteBoardResponse,AddMemberModel,UpdateMemberModel,BoardMemberResponse
from commands.boards import CreateBoardCommand,UpdateBoardCommand,DeleteBoardCommand,AddBoardMemberCommand,UpdateBoardMemberRoleCommand,RemoveBoardMemberCommand
from queries.boards import GetBoardQuery,ListBoardsQuery,ListAccessibleBoardsQuery
from queries.feed import ActivityFeedQuery
from queries.handlers import BoardQueryHandler,ActivityQueryHandler
from commands.handlers import BoardCommandHandler,BoardMemberHandler
from sqlalchemy.orm import Session
from db.models import User,Board,BoardMembers
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
    query=ListAccessibleBoardsQuery(current_user.id)
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
    
@router.post("/boards/{board_id}/members",response_model=BoardMemberResponse)
def add_member(board_id:int,payload:AddMemberModel,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    command=AddBoardMemberCommand(board_id=board_id,owner_id=current_user.id,target_user_id=payload.user_id,role=payload.role)
    return BoardMemberHandler(db).handle(command)

@router.patch('/boards/{board_id}/members/{user_id}',response_model=BoardMemberResponse)
def change_role(board_id:int,user_id:int,payload:UpdateMemberModel,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    command=UpdateBoardMemberRoleCommand(board_id=board_id,owner_id=current_user.id,target_user_id=user_id,new_role=payload.role)
    return BoardMemberHandler(db).handle(command)

@router.delete("/boards/{board_id}/members/{user_id}")
def remove_member(board_id:int,user_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    command=RemoveBoardMemberCommand(board_id=board_id,owner_id=current_user.id,target_user_id=user_id)
    BoardMemberHandler(db).handle(command)
    return {"message":"member removed"}

@router.get("/boards/{board_id}/feed")
def get_activity_feed(board_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    query=ActivityFeedQuery(board_id=board_id,user_id=current_user.id)
    return ActivityQueryHandler(db).handle(query)


    







