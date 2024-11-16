import strawberry
import grpc
import os
from app.gRPC import otp_pb2,otp_pb2_grpc
from app.graphql.schemas.OTP import OTPinput,OTPSendResponseType,VerifyOTPType
from dotenv import load_dotenv
load_dotenv()
server_port=os.getenv('AUTH_SERVER')
class OTPMutation():
    @staticmethod
    async def generateAndSendOTP(otp: OTPinput) -> OTPSendResponseType:
        try:
            async with grpc.aio.insecure_channel(server_port) as channel:
                stub = otp_pb2_grpc.OTPServiceStub(channel)
                request = otp_pb2.GenerateOTPRequest(email=otp.email)
                response = await stub.GenerateOTP(request)

                if response.success:
                    print("Success!")
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
            async with grpc.aio.insecure_channel(server_port) as channel:
                stub = otp_pb2_grpc.OTPServiceStub(channel=channel)
                request=otp_pb2.VerifyOTPRequest(email=otp.email,otp=otp.otp)
                
                response = await stub.VerifyOTP(request)
                
                if response.success:
                    print("OK!")
                    return OTPSendResponseType(success=True,message='OTP Verified')
                else:
                    print("Not verified")
                    return OTPSendResponseType(success=False,message="Not Verified")
                    
        except Exception as e:
            print(e)
            return OTPSendResponseType(success=False,message='Server Error!')
            