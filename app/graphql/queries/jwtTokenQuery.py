import strawberry
from fastapi import Request
from app.utils.jwt import jwt
class jwtTokenQuery():
    
    @staticmethod
    async def VerifyToken(self,info)->bool:
        try:
            
            
            pass
        except Exception as e:
            print(e)
            return False;
        
        