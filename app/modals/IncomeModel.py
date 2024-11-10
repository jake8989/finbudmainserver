from pydantic import BaseModel

class IncomeModel(BaseModel):
    username:str
    incomeId:str
    amount:int
    category:str
    description:str
    incomeDate:str
    