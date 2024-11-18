import strawberry
from app.graphql.schemas.UserSchema import UserType
from typing import Optional
@strawberry.input
class OTPinput():
    email:str
    
    
    
@strawberry.type    
class OTPSendResponseType():  
    success:bool
    message:str
    user:Optional[UserType]=None
    
@strawberry.input
class VerifyOTPType():
    email:str
    otp:str    