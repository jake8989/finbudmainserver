import strawberry
from app.db.config import database
from app.graphql.schemas.ExpenseSchema import ExpenseGetCategoriesResponseType


class ExpenseQuery:
    @staticmethod
    async def getAllExpenseCategories(
        self, username: str
    ) -> ExpenseGetCategoriesResponseType:
        try:
            user = await database.db["users"].find_one({"username": username})
            if not user:

                return ExpenseGetCategoriesResponseType(
                    success=False, userExpenseCategories=[]
                )

            expenseCategories = user.get("expenseCategories", [])
            # print(expenseCategories)

            return ExpenseGetCategoriesResponseType(
                success=True, userExpenseCategories=expenseCategories
            )
        except Exception as e:
            ExpenseGetCategoriesResponseType(
                success=False, userExpenseCategories=expenseCategories
            )
