import strawberry
from app.graphql.schemas.UserSchema import UserType 
from app.graphql.mutations.userMutation import UserMutations
from app.graphql.mutations.userMutation import UserMutationResponse
@strawberry.type
class Mutation:
    registerUser: UserMutationResponse = strawberry.mutation(resolver=UserMutations.registerUser)
    loginUser:UserMutationResponse = strawberry.mutation(resolver=UserMutations.loginUser)