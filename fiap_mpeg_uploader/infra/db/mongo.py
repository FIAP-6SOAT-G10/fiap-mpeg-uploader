from sys import warnoptions
from motor.motor_asyncio import AsyncIOMotorClient
from fiap_mpeg_uploader.infra.db.client import DatabaseClient
from fiap_mpeg_uploader.infra.env.env import EnvManager
from typing import Optional

class MongoClient(DatabaseClient):
    _instance: Optional["MongoClient"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, client: AsyncIOMotorClient):
        if not hasattr(self, "initialized"):  # Prevent reinitialization
            self.client: AsyncIOMotorClient = client
            self.db = self.client["uploader_db"]
            self.initialized = True
    
    @staticmethod
    def build() -> 'MongoClient':
        mongo_uri = EnvManager().get("MONGO_URL")

        client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_uri)
        return MongoClient(client)
    
    async def create(self, table, data):
        result = await self.db[table].insert_one(data)
        return result
    
    async def read(self, table, query):
        result = await self.db[table].find_one(query)
        return result
    
    async def update(self, table, query, data):
        result = await self.db[table].update_many(query, {"$set": data})
        return result

    async def delete(self, table, query):
        result = await self.db[table].delete_many(query)
        return result

