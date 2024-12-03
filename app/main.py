import os
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from app.db.config import database
from contextlib import asynccontextmanager
from app.graphql.graphql import Mutation, Query
from fastapi.middleware.cors import CORSMiddleware
from app.graphql.queries.chartQuery import accumulatedDataInput

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.close()


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

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
