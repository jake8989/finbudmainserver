import strawberry
from typing import Optional, List


@strawberry.input
class accumulatedDataInput:
    year: str
    username: str


@strawberry.type
class cateogoryWiseExpense:
    label: str
    data: List[float]


@strawberry.type
class categoryWiseMonthlyExpensesResponse:
    success: bool
    message: str
    categoryWiseExpenses: Optional[List[cateogoryWiseExpense]] = None


@strawberry.type
class incomeType:
    amount: float
    incomeDate: str


@strawberry.type
class expenseType:
    amount: float
    expenseDate: str


@strawberry.type
class accumulatedDataResponseType:
    success: bool
    message: str
    income: Optional[List[float]] = None
    expense: Optional[List[float]] = None
