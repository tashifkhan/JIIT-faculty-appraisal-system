from typing import Dict, List, Optional
import logging
from app.db.mongo import mongo_client, settings

logger = logging.getLogger(__name__)


class FacultyDataService:
    def __init__(self):
        self.collection_name = settings.FACULTY_DATA_COLLECTION_NAME

    async def get_all_faculty_data(self) -> List[Dict]:
        try:
            return await mongo_client.find_all(
                self.collection_name,
                projection={"_id": 0, "updated_at": 0, "created_at": 0},
            )
        except Exception as e:
            logger.error(f"Error getting faculty data collection: {e}")
            raise e

    async def get_faculty_data_by_user_id(self, user_id: str) -> Optional[Dict]:
        try:
            return await mongo_client.find_one(
                self.collection_name,
                {"user_id": user_id},
                projection={"_id": 0, "updated_at": 0, "created_at": 0},
            )
        except Exception as e:
            logger.error(f"Error getting faculty data by user id: {e}")
            raise e

    async def insert_faculty_data(self, data: Dict):
        try:
            await mongo_client.insert_one(self.collection_name, data)
            logger.info("Faculty data inserted successfully")
        except Exception as e:
            logger.error(f"Error inserting faculty data: {e}")
            raise e
