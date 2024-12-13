import strawberry
import grpc, grpc_tools
import os
from app.gRPC import reports_pb2, reports_pb2_grpc
from app.graphql.schemas.reportSchema import ReportInput, ReportResponse

report_port = os.getenv("REPORT_SERVER")


@strawberry.type
class ReportsQuery:
    @staticmethod
    async def generateReport(self, report: ReportInput) -> ReportResponse:
        print("Main server awaiting")
        print(report)
        async with grpc.aio.insecure_channel(report_port) as channel:
            stub = reports_pb2_grpc.ReportServiceStub(channel=channel)
            request = reports_pb2.ReportRequest(
                username=report.username, year=report.year, month=report.month
            )
            reponse = await stub.GenerateReport(request)
            print(reponse)

        return ReportResponse(success=True, message="Testing Completed")
