from db.models import BoardRole
class CreateBoardCommand:
    def __init__(self,name:str,description:str,user_id:int):
        self.name=name
        self.description=description
        self.user_id=user_id


class UpdateBoardCommand:
    def __init__(self,board_id:int,user_id:int,name=None,description=None):
        self.board_id = board_id
        self.user_id = user_id
        self.name = name
        self.description = description


class DeleteBoardCommand:
    def __init__(self,board_id:int,user_id:int):
        self.board_id=board_id
        self.user_id=user_id


class AddBoardMemberCommand:
    def  __init__(self,board_id:int,owner_id:int,target_user_id:int,role:BoardRole):
        self.board_id=board_id
        self.owner_id=owner_id
        self.target_user_id=target_user_id
        self.role=role

class RemoveBoardMemberCommand:
    def __init__(self,board_id:int,owner_id:int,target_user_id:int):
        self.board_id=board_id
        self.owner_id=owner_id
        self.target_user_id=target_user_id


class UpdateBoardMemberRoleCommand:
    def __init__(self,board_id:int,owner_id:int,target_user_id:int,new_role:BoardRole):
        self.board_id=board_id
        self.owner_id=owner_id
        self.target_user_id=target_user_id
        self.new_role=new_role
