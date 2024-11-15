from motor.motor_asyncio import  AsyncIOMotorClient

import os
class Database:
    def __init__(self):
        self.client=None
        self.db=None
    async def connect(self):
        self.client=AsyncIOMotorClient(os.getenv('DB_URL'))
        self.db=self.client.get_database()
        print('Mongo Connected...')
    async def close(self):
        if self.client:
            self.client.close()   
            print('Mongo Disconnected!') 


database=Database()

