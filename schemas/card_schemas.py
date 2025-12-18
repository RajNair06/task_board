from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional
class CardCreate(BaseModel):
    
    title:str
    description:str
    position:float

    model_config=ConfigDict(from_attributes=True)

class CardOut(BaseModel):
    id:int
    title:str
    description:str
    is_complete:bool
    board_id:int
    position:float
    created_by:int
    created_at:datetime
    updated_at:datetime

    model_config=ConfigDict(from_attributes=True)

class CardUpdate(BaseModel):
    
    title:Optional[str]=None
    description:Optional[str]=None
    position:Optional[float]=None

    model_config=ConfigDict(from_attributes=True)

class DeleteCardResponse(BaseModel):
    name:str
    message:str="Card deleted successfully!"


    
    