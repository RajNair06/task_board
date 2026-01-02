from db.models import BoardMembers,BoardRole
from fastapi import HTTPException,status
class BoardPermissionService:
    @staticmethod
    def require_member(db,board_id:int,user_id:int):
        membership=(db.query(BoardMembers).filter(BoardMembers.board_id==board_id,BoardMembers.user_id==user_id).first())
        if not membership:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not a board member")
        
        return membership
    
    @staticmethod
    def require_role(db,board_id:int,user_id:int,allowed_roles:set[BoardRole]):
        membership=BoardPermissionService.require_member(db,board_id,user_id)
        if membership.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="insufficient permissions")
        
        return membership