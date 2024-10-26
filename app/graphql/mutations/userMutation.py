import strawberry
from app.graphql.schemas.UserSchema import UserType,UserInput
from app.db.config import database
from pydantic import BaseModel
from typing import Optional
from app.modals.UserModal import UserModal

@strawberry.type
class RegisterUserMutationResponse:
    success:bool
    message:str
    user:Optional[UserType]=None

class UserMutations:
    @staticmethod
    async def registerUser(self,user:UserInput)->RegisterUserMutationResponse:
        try:
            existing_user=await database.db['users'].find_one({"username":user.username})
            if existing_user:
                return RegisterUserMutationResponse(success=False,message='Username Already in use')
            
            new_user=UserModal(
                username=user.username,
                email=user.email,
                password=user.password,
                settedGoals=0,
                goals=[]
            )
            print(new_user)
            await database.db['users'].insert_one(new_user.model_dump(by_alias=True))
            return RegisterUserMutationResponse(success=True,message='User Created Successfully',user=UserType(username=new_user.username,email=new_user.email))

        except Exception as e:
            return RegisterUserMutationResponse(success=False,message=e)
