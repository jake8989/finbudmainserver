import strawberry
import grpc
import os
from app.gRPC import otp_pb2,otp_pb2_grpc
from app.graphql.schemas.OTP import OTPinput,OTPSendResponseType,VerifyOTPType
from dotenv import load_dotenv
from app.modals.UserModel import UserModal
from app.modals.OTPRateModel import OTPRateLimitModel
from app.db.config import database
from app.graphql.schemas.UserSchema import UserType

load_dotenv()
server_port=os.getenv('AUTH_SERVER')
class OTPMutation():
    @staticmethod
    async def generateAndSendOTP(otp: OTPinput) -> OTPSendResponseType:
        try:
            if otp.email=='' or not otp.email:
                OTPSendResponseType(success=False,message="Please Provide Email!")
                
            async with grpc.aio.insecure_channel(server_port) as channel:
                stub = otp_pb2_grpc.OTPServiceStub(channel)
                request = otp_pb2.GenerateOTPRequest(email=otp.email)
                response = await stub.GenerateOTP(request)
                
                new_otp_ratelimit=OTPRateLimitModel(
                    email=otp.email,
                    times=0
                )

                exits_otp_ratelimiter=await database.db['otp_rate_limiters'].find_one({"email":otp.email})
                if exits_otp_ratelimiter:
                    if exits_otp_ratelimiter['times']>4:
                        return OTPSendResponseType(success=False,message="OTP generation limit exceeds! please use other email!")
                
                if response.success:
                    print("Success!")
                    if not exits_otp_ratelimiter:
                       await database.db['otp_rate_limiters'].insert_one(new_otp_ratelimit.model_dump(by_alias=True))
                       
                    if exits_otp_ratelimiter:
                        await database.db['otp_rate_limiters'].update_one({"email":otp.email},{"$set":{"times":exits_otp_ratelimiter['times']+1}})
                    
                    return OTPSendResponseType(success=True, message="OTP Sent")
                else:
                    print("Failed to send OTP")
                    return OTPSendResponseType(success=False, message=response.message)

        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")
            return OTPSendResponseType(success=False, message=f"gRPC Error: {e.details()}")

        except Exception as e:
            print(f"Unexpected error: {e}")
            return OTPSendResponseType(success=False, message=f"Error: {str(e)}")
    
    
    @staticmethod    
    async def verifyOTP(otp:VerifyOTPType)->OTPSendResponseType:
        try:
            if otp.email=='' or (not otp.email):
                OTPSendResponseType(success=False,message="Please Provide Email!")
                
            async with grpc.aio.insecure_channel(server_port) as channel:
                stub = otp_pb2_grpc.OTPServiceStub(channel=channel)
                request=otp_pb2.VerifyOTPRequest(email=otp.email,otp=otp.otp)
                
                response = await stub.VerifyOTP(request)
                
                if response.success:
                    print("OK!")
                    temp_user=await database.db['temp_users'].find_one({"email":otp.email})
                    exist_user=await database.db['users'].find_one({"email":otp.email})
                    if exist_user:
                        return OTPSendResponseType(success=False,message="User Exists!")
                    if not temp_user:
                        return OTPSendResponseType(success=False,message="Please Use new OTP")
                     
                     
                    new_user =UserModal(
                        username=temp_user['username'].upper(),
                        email=temp_user['email'],
                        password=temp_user['password'],
                        settedGoals=temp_user['settedGoals'],
                        goals=temp_user['goals'],
                        expenseCategories=temp_user['expenseCategories'] 
                    )
                    
                    await database.db['users'].insert_one(new_user.model_dump(by_alias=True))
                    
                    return OTPSendResponseType(success=True,message='OTP Verified',user=UserType(username=new_user.username,email=new_user.email))
                else:
                    print("Not verified")
                    return OTPSendResponseType(success=False,message="OTP Not Verified")
                    
        except Exception as e:
            print(e)
            return OTPSendResponseType(success=False,message='Server Error!')
            