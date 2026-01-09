class GetBoardQuery:
    def __init__(self,id:int,user_id:int):
        self.id=id
        self.user_id=user_id

class ListBoardsQuery:
    def __init__(self,user_id:int):
        self.user_id=user_id


class ListAccessibleBoardsQuery:
    def __init__(self,user_id:int):
        self.user_id=user_id

class ActivityFeedQuery:
    def __init__(self,board_id:int,user_id:int):
        self.board_id=board_id
        self.user_id=user_id