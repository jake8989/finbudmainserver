import strawberry
from typing import List,Optional
from enum import Enum


@strawberry.enum
class GoalType(str,Enum):
     SAVING='saving'
     EXPENSE='expense'

@strawberry.type
class GoalType():
    goalId:str
    username:str
    goalAmount:int
    startDate:str
    endDate:str
    description:Optional[str]=None
    goalCategory:GoalType

@strawberry.type
class UserType():
    username:str
    email:str


@strawberry.input
class UserInput():
    username:str
    email:str
    password:str
