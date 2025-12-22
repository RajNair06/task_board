class GetCardQuery:
    def __init__(self,id:int,board_id:int,user_id:int):
        self.id=id
        self.board_id=board_id
        self.user_id=user_id

    
class ListCardQuery:
    def __init__(self,board_id:int,user_id:int):
        self.board_id=board_id
        self.user_id=user_id
        