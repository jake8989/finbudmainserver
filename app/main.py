import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.db.config import database
from contextlib import asynccontextmanager
load_dotenv()
@asynccontextmanager
async def lifespan(app:FastAPI):
    await database.connect()
    yield 
    await database.close()

# print(os.getenv('DB_URL'))
app=FastAPI(lifespan=lifespan)
@app.get('/')
async def root():
    return 'Hii the server is working fine'