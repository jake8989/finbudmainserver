from pydantic import BaseModel

class OTPRateLimitModel(BaseModel):
    email:str
    times:int