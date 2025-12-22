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


