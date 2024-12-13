from pydantic import BaseModel


class IncomeModel(BaseModel):
    username: str
    incomeId: str
    amount: float
    category: str
    description: str
    incomeDate: str
