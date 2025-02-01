from pydantic import BaseModel
from typing import List
class Transform(BaseModel):
    name:str
    position:List[float]
    rotation:List[float]
    scale:List[float]
class Component(BaseModel):
    name:str
    data:List[float]
class AddItem(BaseModel):
    name:str
    qty:int
class updateItem(BaseModel):
    name:str
    new_qty:int
class deleteItem(BaseModel):
    name:str