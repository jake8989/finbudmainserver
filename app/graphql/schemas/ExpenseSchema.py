import strawberry
from typing import Optional,List

@strawberry.type
class ExpenseResponseType():
    success:bool
    message:str
    expenseId:Optional[str]=None

@strawberry.input
class ExpenseInput():
    username:str
    amount:int
    category:str
    expenseDate:str



@strawberry.type
class ExpenseGetCategoriesResponseType():
    success:bool
    userExpenseCategories:List[str]=None



@strawberry.input
class ExpenseCategoryInput():
    username:str
    expenseCategory:str