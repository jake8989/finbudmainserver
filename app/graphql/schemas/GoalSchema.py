import strawberry
from typing import Optional
@strawberry.input
class GoalInput():
    username:str
    goalAmount:int
    goalDescription:str
    goalStartDate:str
    goalEndDate:str
    goalCategory:str
    goalReminderFreq:str
    goalType:str
    
    
@strawberry.input
class DeleteGoalInputType():
    goalId:str
    username:str

@strawberry.type
class GoalType():
    goalId:str
    goalAmount:int
    goalDescription:str
    goalStartDate:str
    goalEndDate:str
    goalCategory:str
    goalType:str
    goalReminderFreq:str



@strawberry.type
class GoalReponseType():
    success:bool
    message:str
    goal:Optional[GoalType]=None
    