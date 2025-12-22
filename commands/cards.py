class CreateCardCommand:
    def __init__(self,board_id:int,user_id:int,position:float,title:str,description:str):
        
        self.board_id=board_id
        self.user_id=user_id
        self.title=title
        self.position=position
        self.description=description


class UpdateCardCommand:
    def __init__(self,id:int,board_id:int,user_id:int,position=None,title=None,description=None):
        self.id=id
        self.board_id=board_id
        self.user_id=user_id
        self.position=position
        self.title=title
        self.description=description

class DeleteCardCommand:
    def __init__(self,id,board_id,user_id):
        self.id=id
        self.board_id=board_id
        self.user_id=user_id
    

        

