import os
import io
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI, HTTPException, Query as QueryParameters
from dotenv import load_dotenv
from app.db.config import database
from contextlib import asynccontextmanager
from app.graphql.graphql import Mutation, Query
from fastapi.middleware.cors import CORSMiddleware
from app.graphql.queries.chartQuery import accumulatedDataInput
from fastapi.responses import StreamingResponse

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.close()


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema, graphiql=True)

# print(os.getenv('DB_URL'))
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return HTTPException(status_code=404, detail="No Users Found")


@app.get("/test")
def hello():
    return {"message": "test"}


@app.get("/downloadReport")
async def downloadReport(report_id: str = QueryParameters(...)):
    try:
        # print("report_id", report_id)
        report_data = await database.db["reports"].find_one({"reportId": report_id})
        pdf_binary_data = report_data["pdf_data"]
        if not pdf_binary_data:
            return ValueError("Generated file is empty")

        pdf_file = io.BytesIO(pdf_binary_data)
        file_name = f"{report_id}-generatedreport.pdf"
        return StreamingResponse(
            pdf_file,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
        )

    except ValueError as e:
        print(e)
        return HTTPException(status_code=400, detail=f"Error in file generation {e}")
    except Exception as e:
        print(e)
        return HTTPException(status_code=400, detail=f"Error in file generation {e}")
