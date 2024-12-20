import strawberry
from typing import List, Optional


@strawberry.input
class ReportInput:
    username: str
    year: str
    month: str


@strawberry.type
class ReportResponse:
    success: bool
    message: str
    reportId: str


@strawberry.type
class downloadReportInput:
    reportId: str
    username: str
