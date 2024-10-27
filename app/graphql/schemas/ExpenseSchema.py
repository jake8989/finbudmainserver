import strawberry
from typing import Optional
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


