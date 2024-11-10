import strawberry
from app.db.config import database
from app.graphql.schemas.IncomeSchema import IncomeInputType,AddIncomeResponseType
from app.modals.IncomeModel import IncomeModel
import uuid
@strawberry.type
class IncomeMutation():
    @staticmethod
    async def createIncome(income:IncomeInputType)->AddIncomeResponseType:
        try:
            exist_user=await database.db['users'].find_one({"username":income.username})
            if not exist_user:
                return AddIncomeResponseType(success=False,message="No user Exists")
            
            newIncome=IncomeModel(
                incomeId=str(uuid.uuid4()),
                username=income.username,
                amount=int(income.amount),
                category=income.category,
                incomeDate=income.incomeDate,
                description=income.description
            )
            await database.db['incomes'].insert_one(newIncome.model_dump(by_alias=True))
            return AddIncomeResponseType(success=True,message="Income Added Successfully",incomeId=newIncome.incomeId)
        except Exception as e:
            print(e)
            return AddIncomeResponseType(success=False,message="Database Error!")