import strawberry
import uuid
from fastapi import Request
from app.graphql.schemas.ExpenseSchema import ExpenseInput,ExpenseResponseType,ExpenseCategoryInput
from app.modals.ExpenseModel import Expense
from app.db.config import database
from app.utils.jwt import JwtToken
@strawberry.type
class ExpenseCategoryResponse():
    success:bool
    message:str


class ExpenseMutation():
    @staticmethod
    async def createExpense(self,expense:ExpenseInput)->ExpenseResponseType:
        try:
            new_expense=Expense(
                expenseId=str(uuid.uuid4()),
                username=expense.username,
                amount=expense.amount,
                category=expense.category,
                description=expense.description,
                expenseDate=expense.expenseDate
            )

            await database.db['expenses'].insert_one(new_expense.model_dump(by_alias=True))
            # print(created_expense)

            return ExpenseResponseType(success=True,message='Expense Created Successfully!',expenseId=new_expense.expenseId)


        except Exception as e:
            print(e)   
            return ExpenseResponseType(success=False,message='Server Error') 

    


    @staticmethod
    async def createNewExpenseCategory(self,expenseCategory:ExpenseCategoryInput)->ExpenseCategoryResponse:
        try:
            existUser=await database.db['users'].find_one({"username":expenseCategory.username})
            ## secure this path
            allExpenseCategories=existUser['expenseCategories']
            newCategory=expenseCategory.expenseCategory.upper()


            if newCategory in allExpenseCategories:
                return ExpenseCategoryResponse(success=False,message="Expense Category Already Exists!")
            

            #append 
            allExpenseCategories.append(newCategory)
            await database.db['users'].update_one({"username":expenseCategory.username},{"$set":{"expenseCategories":allExpenseCategories}})
            return ExpenseCategoryResponse(success=True,message='Expense Category Added Succesfully')  
            
        except Exception as e:
            print(e)     
            return ExpenseCategoryResponse(success=False,message=e)  

    @staticmethod
    async def deleteExistExpenseCategory(self,expenseCategory:ExpenseCategoryInput)->ExpenseCategoryResponse:
        try:
            existUser=await database.db['users'].find_one({"username":expenseCategory.username})
            if not existUser:
                return ExpenseCategoryResponse(success=False,message='User Not Found!')
               
            
            allExpenseCategories=existUser.expenseCategories
            expenseCategoryToBeDeleted=expenseCategory.expenseCategory
            if expenseCategoryToBeDeleted in allExpenseCategories:
                updated_categories=[cat for cat in allExpenseCategories if cat!=expenseCategoryToBeDeleted]
                await database.db['users'].update_one({"username":expenseCategory.username},{"$set":{"expenseCategories":updated_categories}})
                return ExpenseCategoryResponse(success=True,message='Expense Category Removed!')
            


            return ExpenseCategoryResponse(success=False,message="Expense Category Not Found!")


        except Exception as e:
            print(e) 
            return ExpenseCategoryResponse(success=False,message=e)
                    



