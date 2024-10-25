import os
from fastapi import FastAPI,HTTPException
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
    users_collection=database.db['users']
    allUsers=await users_collection.find({},{"_id":0}).to_list()
    if allUsers:
       return allUsers
    return HTTPException(status_code=404,detail='No Users Found')