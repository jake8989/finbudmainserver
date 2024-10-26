import strawberry
from app.graphql.schemas.UserSchema import UserType 
from app.graphql.mutations.userMutation import UserMutations
from app.graphql.mutations.userMutation import RegisterUserMutationResponse
@strawberry.type
class Mutation:
    registerUser: RegisterUserMutationResponse = strawberry.mutation(resolver=UserMutations.registerUser)