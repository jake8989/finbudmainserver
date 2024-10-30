import strawberry
from app.graphql.schemas.UserSchema import UserType 
from app.graphql.mutations.userMutation import UserMutations
from app.graphql.mutations.userMutation import UserMutationResponse
from app.graphql.mutations.expenseMutation import ExpenseMutation,ExpenseCategoryResponse
from app.graphql.schemas.ExpenseSchema import ExpenseResponseType,ExpenseGetCategoriesResponseType
from app.graphql.queries.testQuery import TestQuery
from app.graphql.queries.expenseQuery import ExpenseQuery

# from app.graphql.queries.testQuery import 
@strawberry.type
class Mutation:
    registerUser: UserMutationResponse = strawberry.mutation(resolver=UserMutations.registerUser)
    loginUser:UserMutationResponse = strawberry.mutation(resolver=UserMutations.loginUser)
    createExpense:ExpenseResponseType=strawberry.mutation(resolver=ExpenseMutation.createExpense)
    createExpenseCategory:ExpenseCategoryResponse=strawberry.mutation(resolver=ExpenseMutation.createNewExpenseCategory)

@strawberry.type
class Query:
    testQuery:str=strawberry.mutation(resolver=TestQuery.testQuery)
    getAllExpenseCategories:ExpenseGetCategoriesResponseType=strawberry.mutation(resolver=ExpenseQuery.getAllExpenseCategories)
