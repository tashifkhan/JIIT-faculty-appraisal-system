import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

logger = logging.getLogger(__name__)


class AsyncMongoDBClient:
    client: AsyncIOMotorClient = None
    db = None

    def connect(self):
        try:
            self.client = AsyncIOMotorClient(
                settings.MONGO_URI, maxPoolSize=100, minPoolSize=10
            )
            self.db = self.client[settings.APPRAISAL_SYSTEM_MONGO_DB_NAME]
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e

    def close(self):
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB connection")

    async def find_one(
        self, collection_name: str, filter: dict, projection: dict = None
    ):
        try:
            collection = self.db[collection_name]
            return await collection.find_one(filter, projection)
        except Exception as e:
            logger.error(f"Error finding document in {collection_name}: {e}")
            raise e

    async def update_one(
        self, collection_name: str, filter: dict, update: dict, upsert: bool = False
    ):
        try:
            collection = self.db[collection_name]
            return await collection.update_one(filter, update, upsert=upsert)
        except Exception as e:
            logger.error(f"Error updating document in {collection_name}: {e}")
            raise e

    async def find_all(
        self, collection_name: str, filter: dict = None, projection: dict = None
    ):
        try:
            collection = self.db[collection_name]
            cursor = collection.find(filter or {}, projection)
            return await cursor.to_list(length=None)
        except Exception as e:
            logger.error(f"Error finding documents in {collection_name}: {e}")
            raise e


mongo_client = AsyncMongoDBClient()
