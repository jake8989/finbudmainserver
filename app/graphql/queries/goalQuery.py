import strawberry
from app.db.config import database
from app.graphql.schemas.GoalSchema import AllUserGoalsResponseType
from app.graphql.schemas.GoalSchema import GoalType
from fastapi import HTTPException
@strawberry.type
class GoalQuery():
    @staticmethod
    async def getAllUserGoals(username:str)->AllUserGoalsResponseType:
        try:
            exists_user=await database.db['users'].find_one({"username":username})
            if exists_user:
                allGoals=exists_user.get('goals',[])
                all_user_goals = [GoalType(**goal) for goal in allGoals]
                return AllUserGoalsResponseType(success=True, allUserGoals=all_user_goals)

            # return HTTPException(status_code=404, detail="Goal not found")
            return AllUserGoalsResponseType(success=False)
        except Exception as e:
            print(e)
            return AllUserGoalsResponseType(success=False)
    