import strawberry
import grpc, grpc_tools
import os
from app.gRPC import reports_pb2, reports_pb2_grpc
from app.graphql.schemas.reportSchema import ReportInput, ReportResponse
from app.db.config import database
from fastapi.responses import StreamingResponse
from app.graphql.schemas.reportSchema import downloadReportInput
from fastapi import HTTPException
import io

report_port = os.getenv("REPORT_SERVER")


@strawberry.type
class ReportsMutation:
    @staticmethod
    async def generateReport(self, report: ReportInput) -> ReportResponse:
        # print("Main server awaiting")
        print(report)
        try:
            async with grpc.aio.insecure_channel(report_port) as channel:
                stub = reports_pb2_grpc.ReportServiceStub(channel=channel)
                request = reports_pb2.ReportRequest(
                    username=report.username, year=report.year, month=report.month
                )
                reponse = await stub.GenerateReport(request)
                # print(reponse)
                ##############################################################
                # ? this report id says that there is no expenses
                if reponse.report_id == "?":
                    return ReportResponse(
                        success=False,
                        message="No Expenses Found for Selected Data!",
                        reportId=reponse.report_id,
                    )
                ##############################################################
                if reponse.success:

                    user_report = await database.db["reports"].find_one(
                        {"reportId": reponse.report_id}
                    )
                    # print(user_report.reportId)
                    pdf_binary_data = user_report["pdf_data"]

                    with open(f"app/reports/{report.username}.pdf", "wb") as f:
                        f.write(pdf_binary_data)

                    return ReportResponse(
                        success=True,
                        message="Report Generated Successfully!",
                        reportId=reponse.report_id,
                    )
                else:
                    return ReportResponse(
                        success=False,
                        message="Error with the report service",
                        reportId="$",
                    )
        except Exception as e:
            print(e)
            return ReportResponse(
                success=False,
                message="Error with the report service",
                reportId="$",
            )

    # @staticmethod
