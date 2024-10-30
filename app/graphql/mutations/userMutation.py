import strawberry
from app.graphql.schemas.UserSchema import UserType,UserInput,UserLoginInput
from app.db.config import database
from pydantic import BaseModel
from typing import Optional
from app.modals.UserModal import UserModal
from app.utils.passwordHasher import PasswordHasher
from app.utils.jwt import JwtToken
@strawberry.type
class UserMutationResponse:
    success:bool
    message:str
    token:Optional[str]=None
    user:Optional[UserType]=None

class UserMutations:
    @staticmethod
    async def registerUser(self,user:UserInput)->UserMutationResponse:
        try:
            existing_user=await database.db['users'].find_one({"username":user.username})
           
            
            if existing_user:
                return UserMutationResponse(success=False,message='Username Already in use')
            #pydentic modal for extra type and shape safety
            hashedPassword=await PasswordHasher.Hash(user.password)
            new_user=UserModal(
                username=user.username,
                email=user.email,
                password=hashedPassword,
                settedGoals=0,
                goals=[],
                expenseCategories=[]
            )

            token=await JwtToken.CreateToken({"username":user.username})

            await database.db['users'].insert_one(new_user.model_dump(by_alias=True))

            return UserMutationResponse(success=True,message='User Created Successfully',token=token, user=UserType(username=new_user.username,email=new_user.email))
        except Exception as e:
            return UserMutationResponse(success=False,message=e)
            
        
    @staticmethod
    async def loginUser(self,user:UserLoginInput)->UserMutationResponse:
        try:
           # find weather this user exists or not with username
           exist_user=await database.db['users'].find_one({"username":user.username})
           print(user)
           if exist_user:
               verify_password=await PasswordHasher.VerifyPassword(password=user.password,hashedPassword=exist_user['password'])
               if verify_password:
                   token=await JwtToken.CreateToken({"username":exist_user['username']})
                   return UserMutationResponse(success=True,message="Logged In Successfully",token=token,user=UserType(username=exist_user['username'],email=exist_user['email']))

               return UserMutationResponse(success=False,message='Invalid Credentails')    
               

           return UserMutationResponse(success=False,message='User not found!')     


           

        except Exception as e:
            return UserMutationResponse(success=False,message=e)


