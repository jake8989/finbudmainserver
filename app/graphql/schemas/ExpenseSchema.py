import strawberry
from typing import Optional, List


@strawberry.type
class ExpenseResponseType:
    success: bool
    message: str
    expenseId: Optional[str] = None


@strawberry.input
class ExpenseInput:
    username: str
    amount: float
    category: str
    description: str
    expenseDate: str


@strawberry.input
class GoalInput:
    goalAmount: float
    goalDescription: str
    goalStartDate: str
    goalEndDate: str
    goalCategory: str
    goalReminderFreq: str
    goalType: str


@strawberry.type
class ExpenseGetCategoriesResponseType:
    success: bool
    userExpenseCategories: List[str] = None


@strawberry.input
class ExpenseCategoryInput:
    username: str
    expenseCategory: str
