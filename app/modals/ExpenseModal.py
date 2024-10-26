from pydantic import BaseModel

class Expense(BaseModel):
    expenseId:int
    category:str
    date:str
    amount:int
