from pydantic import BaseModel

class Expense(BaseModel):
    expenseId:str
    username:str
    amount:int
    category:str
    expenseDate:str
