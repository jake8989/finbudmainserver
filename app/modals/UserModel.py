from pydantic import BaseModel,Field
from typing import List,Optional
from enum import Enum
from app.graphql.schemas.GoalSchema import GoalType
from datetime import datetime
class GoalCategory(str,Enum):
     SAVING='saving'
     EXPENSE='expense'
      
class ExpenseCategories(BaseModel):
    expenseId:str
    expenseType:str


    

class UserModal(BaseModel):
    username:str
    email:str
    password:str
    settedGoals:int=0
    goals:List[GoalType]=[]
    expenseCategories:List[ExpenseCategories]=[]
    
    
class TempUserModal(BaseModel):
    username:str
    email:str
    password:str
    settedGoals:int=0
    goals:List[GoalType]=[]
    expenseCategories:List[ExpenseCategories]=[]
    expiresAt:datetime
        