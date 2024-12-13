import strawberry
from app.graphql.schemas.UserSchema import UserType, UserInput, UserLoginInput
from app.db.config import database
from pydantic import BaseModel
from typing import Optional
from app.modals.UserModel import UserModal, TempUserModal
from app.utils.passwordHasher import PasswordHasher
from app.utils.jwt import JwtToken
from datetime import datetime, time, timedelta, timezone
from pymongo import ASCENDING


@strawberry.type
class UserMutationResponse:
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[UserType] = None


class UserMutations:
    @staticmethod
    async def registerUser(self, user: UserInput) -> UserMutationResponse:
        try:
            existing_user = await database.db["users"].find_one(
                {"username": user.username.upper()}
            )
            existing_email = await database.db["users"].find_one({"email": user.email})
            if existing_email:
                return UserMutationResponse(
                    success=False, message="Email Already in use"
                )

            if existing_user:
                return UserMutationResponse(
                    success=False, message="Username Already in use"
                )
            # pydentic modal for extra type and shape safety
            hashedPassword = await PasswordHasher.Hash(user.password)
            # datetime.utcnow()
            expiresAt = datetime.now(timezone.utc) + timedelta(seconds=300)
            # creating temporary user in the db so that after otp verification
            # we can create a persistance entry in the mongoDB
            new_user = TempUserModal(
                username=user.username.upper(),
                email=user.email,
                password=hashedPassword,
                settedGoals=0,
                goals=[],
                expenseCategories=[],
                expiresAt=expiresAt,
            )
            await database.db["temp_users"].create_index(
                [("expiresAt", ASCENDING)], expireAfterSeconds=0
            )

            # token=await JwtToken.CreateToken({"username":user.username})

            await database.db["temp_users"].insert_one(
                new_user.model_dump(by_alias=True)
            )

            return UserMutationResponse(
                success=True,
                message="Proceed With OTP",
                user=UserType(username=new_user.username, email=new_user.email),
            )
        except Exception as e:
            return UserMutationResponse(success=False, message=e)

    @staticmethod
    async def loginUser(self, user: UserLoginInput) -> UserMutationResponse:
        try:
            # find weather this user exists or not with username
            exist_user_username = await database.db["users"].find_one(
                {"username": user.usernameoremail.upper()}
            )
            exist_user_email = await database.db["users"].find_one(
                {"email": user.usernameoremail}
            )
            #    print(user)
            exist_user = {}

            if exist_user_username is not None:
                exist_user = exist_user_username
            elif exist_user_email is not None:
                exist_user = exist_user_email

            if exist_user:
                verify_password = await PasswordHasher.VerifyPassword(
                    password=user.password, hashedPassword=exist_user["password"]
                )
                if verify_password:

                    token = await JwtToken.CreateToken(
                        {"usernameoremail": exist_user["username"]}
                    )
                    return UserMutationResponse(
                        success=True,
                        message="Logged In Successfully",
                        token=token,
                        user=UserType(
                            username=exist_user["username"], email=exist_user["email"]
                        ),
                    )

                return UserMutationResponse(
                    success=False, message="Invalid Credentails"
                )

            return UserMutationResponse(success=False, message="User not found!")

        except Exception as e:
            return UserMutationResponse(success=False, message=e)
