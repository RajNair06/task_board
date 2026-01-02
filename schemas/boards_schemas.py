from pydantic import BaseModel,ConfigDict
from datetime  import datetime
from db.models import BoardRole
from typing import Optional

class BoardCreate(BaseModel):
    name:str
    description:str

    model_config=ConfigDict(from_attributes=True)

class BoardOut(BaseModel):
    id:int
    name:str
    description:str
    created_by:int
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)

class BoardUpdate(BaseModel):
    
    name:Optional[str]=None
    description:Optional[str]=None

    model_config=ConfigDict(from_attributes=True)

class DeleteBoardResponse(BaseModel):
    name:str
    message:str="Board deleted successfully!"


class AddMemberModel(BaseModel):
    user_id:int
    role:BoardRole

class UpdateMemberModel(BaseModel):
    role:BoardRole

class BoardMemberResponse(BaseModel):
    user_id: int
    board_id: int
    role: BoardRole
    
    
    model_config = ConfigDict(from_attributes=True)

    

