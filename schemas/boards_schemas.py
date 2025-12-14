from pydantic import BaseModel
from datetime  import datetime
from typing import Optional

class BoardCreate(BaseModel):
    name:str
    description:str

class BoardOut(BaseModel):
    id:int
    name:str
    description:str
    created_by:int
    created_at:datetime
    updated_at:datetime

    model_config = {"from_attributes": True}

class BoardUpdate(BaseModel):
    id:int
    name:Optional[str]=None
    description:Optional[str]=None

    model_config = {"from_attributes": True}

class BoardDelete(BaseModel):
    pass




    

