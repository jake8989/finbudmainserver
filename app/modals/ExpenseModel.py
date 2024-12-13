from pydantic import BaseModel
from typing import List


class Expense(BaseModel):
    expenseId: str
    username: str
    amount: float
    category: str
    description: str
    expenseDate: str
