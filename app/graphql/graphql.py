import strawberry
from app.graphql.schemas.UserSchema import UserType 
from app.graphql.mutations.userMutation import UserMutations
from app.graphql.mutations.userMutation import UserMutationResponse
from app.graphql.mutations.expenseMutation import ExpenseMutation
from app.graphql.schemas.ExpenseSchema import ExpenseResponseType
@strawberry.type
class Mutation:
    registerUser: UserMutationResponse = strawberry.mutation(resolver=UserMutations.registerUser)
    loginUser:UserMutationResponse = strawberry.mutation(resolver=UserMutations.loginUser)
    createExpense:ExpenseResponseType=strawberry.mutation(resolver=ExpenseMutation.createExpense)