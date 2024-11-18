from datetime import datetime, timezone, timedelta
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from typing import Optional
from dataclasses import dataclass


class JwtToken:
    @staticmethod
    async def CreateToken(data: dict) -> str:
        try:
            encode_with_expiry = data.copy()
            expire_delta = timedelta(hours=24)
            expire = datetime.now(timezone.utc) + expire_delta
            encode_with_expiry.update({"exp": expire})
            
            # Make sure JWT_SECRET is available
            jwt_secret = os.getenv('JWT_SECRET')
            if not jwt_secret:
                return ''
                
            token = jwt.encode(
                encode_with_expiry,
                jwt_secret,
                algorithm='HS256'
            )
            return token
            
        except Exception as e:
            print(f"Error creating token: {str(e)}")
            return ''

    @staticmethod
    async def VerifyToken(token: str):
        try:
            jwt_secret = os.getenv('JWT_SECRET')
           
            if not jwt_secret:
                return None
                
            decoded_token = jwt.decode(
                token,
                jwt_secret,
                algorithms=['HS256']
            )
            return decoded_token
            
        except ExpiredSignatureError:
            print('Token Expired')
            return None
        except InvalidTokenError as e:
            print(f'Invalid Token: {str(e)}')
            return None
        except Exception as e:
            print(f'Error verifying token: {str(e)}')
            return None