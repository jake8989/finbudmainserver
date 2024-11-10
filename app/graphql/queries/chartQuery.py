import strawberry
from app.db.config import database
from app.graphql.schemas.chartSchema import accumulatedDataInput,accumulatedDataResponseType,incomeType,expenseType
# from app.graphql.schemas.chartSchema
@strawberry.type
class ChartQuery():
    @staticmethod
    async def getAccumulatedData(data:accumulatedDataInput)->accumulatedDataResponseType:
        try:
            all_incomes = await database.db['incomes'].find(
                {"username": data.username, "incomeDate": {"$regex": f"^{data.year}"}}
            ).to_list(length=None)
            
            all_expenses = await database.db['expenses'].find(
                {"username": data.username, "expenseDate": {"$regex": f"^{data.year}"}}
            ).to_list(length=None)
            # print(all_incomes,all_expenses)
            income_data=[incomeType(amount=income['amount'],incomeDate=income['incomeDate']) for income in all_incomes]
            expense_data=[expenseType(amount=expense['amount'],expenseDate=expense['expenseDate']) for expense in all_expenses]
            
            monthly_income_data=[0]*13
            monthly_expense_data=[0]*13
            
            for income in income_data:
                month=int(income.incomeDate.split('-')[1])
                monthly_income_data[month]+=income.amount
            
            for expense in expense_data:
                month=int(expense.expenseDate.split('-')[1])
                monthly_expense_data[month]+=expense.amount    
                
                
            # print(monthly_income_data[1:])
            # print(monthly_expense_data[1:])
            
            
            return accumulatedDataResponseType(success=True,message="Ok",income=monthly_income_data[1:],expense=monthly_expense_data[1:])
        except Exception as e:
            print(e)
            return accumulatedDataResponseType(success=False,message="Error")
    