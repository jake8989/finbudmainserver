import strawberry
from app.db.config import database
from app.graphql.schemas.IncomeSchema import IncomeInputType, AddIncomeResponseType
from app.modals.IncomeModel import IncomeModel
import uuid


@strawberry.type
class IncomeMutation:
    @staticmethod
    async def createIncome(income: IncomeInputType) -> AddIncomeResponseType:
        try:
            exist_user = await database.db["users"].find_one(
                {"username": income.username}
            )
            if not exist_user:
                return AddIncomeResponseType(success=False, message="No user Exists")

            newIncome = IncomeModel(
                incomeId=str(uuid.uuid4()),
                username=income.username,
                amount=int(income.amount),
                category=income.category,
                incomeDate=income.incomeDate,
                description=income.description,
            )
            allUserGoals = exist_user["goals"]
            exist_goal_with_same_category = next(
                (g for g in allUserGoals if g["goalCategory"] == income.category), None
            )

            # if exist_goal_with_same_category:
            #     if exist_goal_with_same_category['goalType']=='Saving Goal':
            #         newGoalAmount=exist_goal_with_same_category['goalAmount']+income.amount
            #         if newGoalAmount<0:
            #             newGoalAmount=0

            #         await database.db['users'].update_one({"username":income.username,"goals.goalCategory":exist_goal_with_same_category['goalCategory']},{
            #             "$set":{
            #                 "goals.$.goalAmount":newGoalAmount
            #             }
            #         })
            await database.db["incomes"].insert_one(newIncome.model_dump(by_alias=True))
            return AddIncomeResponseType(
                success=True,
                message="Income Added Successfully",
                incomeId=newIncome.incomeId,
            )
        except Exception as e:
            print(e)
            return AddIncomeResponseType(success=False, message="Database Error!")
