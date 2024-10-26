import strawberry
from app.graphql.schemas.UserSchema import UserType,UserInput
from app.db.config import database
from pydantic import BaseModel
from typing import Optional
from app.modals.UserModal import UserModal
from app.utils.passwordHasher import PasswordHasher
from app.utils.jwt import JwtToken

@strawberry.type
class RegisterUserMutationResponse:
    success:bool
    message:str
    token:Optional[str]=None
    user:Optional[UserType]=None

class UserMutations:
    @staticmethod
    async def registerUser(self,user:UserInput)->RegisterUserMutationResponse:
        try:
            existing_user=await database.db['users'].find_one({"username":user.username})
            if existing_user:
                return RegisterUserMutationResponse(success=False,message='Username Already in use')
            #pydentic modal for extra type and shape safety
            hashedPassword=await PasswordHasher.Hash(user.password)
            new_user=UserModal(
                username=user.username,
                email=user.email,
                password=hashedPassword,
                settedGoals=0,
                goals=[]
            )
            token=await JwtToken.CreateToken({"username":user.username})
            my=await JwtToken.VerifyToken(token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impha2UiLCJleHAiOjE3Mjk5ODEyNjd9.ESJmYwythu2Pv7aXt2hrGz1yWbxLLEBbod1fk0UY2FI')
            print(my)
            await database.db['users'].insert_one(new_user.model_dump(by_alias=True))
            return RegisterUserMutationResponse(success=True,message='User Created Successfully',token=token, user=UserType(username=new_user.username,email=new_user.email))

        except Exception as e:
            return RegisterUserMutationResponse(success=False,message=e)
