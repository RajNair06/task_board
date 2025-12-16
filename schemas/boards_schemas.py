from pydantic import BaseModel,ConfigDict
from datetime  import datetime
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

    




    

