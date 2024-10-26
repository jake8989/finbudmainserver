import os
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI,HTTPException
from dotenv import load_dotenv
from app.db.config import database
from contextlib import asynccontextmanager
from app.graphql.graphql import Mutation
load_dotenv()
@asynccontextmanager
async def lifespan(app:FastAPI):
    await database.connect()
    yield 
    await database.close()


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello From the graphQL"


schema = strawberry.Schema(query=Query,mutation=Mutation)

graphql_app = GraphQLRouter(schema)


# print(os.getenv('DB_URL'))
app=FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")
@app.get('/')
async def root():
    return HTTPException(status_code=404,detail='No Users Found')