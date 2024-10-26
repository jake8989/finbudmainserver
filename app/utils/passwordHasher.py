from passlib.context import CryptContext

passwordContext=CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:
    @staticmethod
    async def VerifyPassword(password,hashedPassword):
        return passwordContext.verify(password,hashedPassword)
    @staticmethod
    async def Hash(password:str):
        return passwordContext.hash(password)
