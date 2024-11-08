import strawberry
from typing import Optional,List
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
class GetAllUserGoalsType():
    username:str

        
@strawberry.input
class DeleteGoalInputType():
    goalId:str
    username:str
    
    
@strawberry.input
class EditGoalInputType():
    goalId:str
    username:str
    goalAmount:Optional[int]=None
    goalEndDate:Optional[str]=None
    goalDescription:Optional[str]=None

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

# @strawberry.type
# class EditGoalType():
    
@strawberry.type
class AllUserGoalsResponseType():
    success:bool
    allUserGoals:Optional[List[GoalType]]=None
        
    

@strawberry.type
class GoalReponseType():
    success:bool
    message:str
    goal:Optional[GoalType]=None
    