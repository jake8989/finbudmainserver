import strawberry
import uuid
from app.graphql.schemas.ExpenseSchema import ExpenseInput,ExpenseResponseType
from app.modals.ExpenseModal import Expense
from app.db.config import database
class ExpenseMutation():
    @staticmethod
    async def createExpense(self,expense:ExpenseInput)->ExpenseResponseType:
        try:
            # print(expense)
    #         expenseId:str
    # username:str
    # amount:int
    # category:str
    # expenseDate:str
            new_expense=Expense(
                expenseId=str(uuid.uuid4()),
                username=expense.username,
                amount=expense.amount,
                category=expense.category,
                expenseDate=expense.expenseDate
            )

            await database.db['expenses'].insert_one(new_expense.model_dump(by_alias=True))
            # print(created_expense)

            return ExpenseResponseType(success=True,message='Expense Created Successfully!',expenseId=new_expense.expenseId)






        except Exception as e:
            print(e)   
            return ExpenseResponseType(success=False,message='Server Error') 





