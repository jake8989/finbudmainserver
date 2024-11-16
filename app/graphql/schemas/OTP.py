import strawberry

@strawberry.input
class OTPinput():
    email:str
    
    
    
@strawberry.type    
class OTPSendResponseType():  
    success:bool
    message:str
    
@strawberry.input
class VerifyOTPType():
    email:str
    otp:str    