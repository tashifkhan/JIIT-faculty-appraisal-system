from fastapi import APIRouter, HTTPException, Query, status
from typing import Dict, Any
from app.services.faculty_data import FacultyDataService

router = APIRouter()
service = FacultyDataService()


@router.get("/get-faculty-data/")
async def get_faculty_data(
    user_id: str = Query(..., description="User ID to fetch faculty data")
):
    try:
        result = await service.get_faculty_data_by_user_id(user_id)
        if result is None:
            # Depending on requirement, could be 404 or just null result.
            # Django returns null result with 200 usually in the view we passed?
            # Django view code: `result = client.get...(user_id)`. If None, it sends None in `result`.
            pass
        return {"message": "Data fetched successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting faculty data")
