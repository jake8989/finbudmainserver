import strawberry
from typing import Optional


@strawberry.input
class IncomeInputType:
    username: str
    amount: float
    category: str
    description: str
    incomeDate: str


# @strawberry.type
# class IncomeType():
#     incomeId:str
#     username:str
#     amount:int
#     category:str
#     description:str
#     incomeDate:str


@strawberry.type
class AddIncomeResponseType:
    success: bool
    message: str
    incomeId: Optional[str] = None
