class GetBoardQuery:
    def __init__(self,id:int,user_id:int):
        self.id=id
        self.user_id=user_id

class ListBoardsQuery:
    def __init__(self,user_id:int):
        self.user_id=user_id


