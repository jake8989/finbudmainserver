import jwt
import os
from datetime import datetime,timedelta,timezone
from jwt import ExpiredSignatureError, InvalidTokenError
class JwtToken:
    @staticmethod
    async def CreateToken(data:dict)->str:
        encode_with_expiry=data.copy()
        expire_delta=timedelta(hours=1)
        expire=datetime.now(timezone.utc)+expire_delta
        encode_with_expiry.update({"exp":expire})

        token=jwt.encode(encode_with_expiry,os.getenv('JWT_SECRET'),algorithm='HS256')
        return token
    
    @staticmethod
    async def VerifyToken(token:str):
        try:
            decoded_token=jwt.decode(token,os.getenv("JWT_SECRET"),algorithm='HS256')
            return decoded_token
 
        except ExpiredSignatureError:
            print('Token Expired')
        except InvalidTokenError:
            print('Invalid Token')
                 
    
