from pydantic import BaseModel,Field
from typing import List,Optional
from enum import Enum

class GoalCategory(str,Enum):
     SAVING='saving'
     EXPENSE='expense'
      
class GoalModal(BaseModel):
    goalId:str
    username:str
    goalAmount:int
    startDate:str
    endDate:str
    description:Optional[str]=None
    goalCategory:GoalCategory
    

class UserModal(BaseModel):
    username:str
    email:str
    password:str
    settedGoals:int=0
    goals:List[GoalModal]=[]