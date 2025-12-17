from fastapi import APIRouter, HTTPException, Query, Body, status
from typing import List, Dict, Any, Optional
from app.services.data_ingestion import DataIngestionService

router = APIRouter()
service = DataIngestionService()


@router.get("/get-item-by-section/")
async def get_item_by_section(
    user_id: str = Query(..., description="User ID"),
    section: str = Query(..., description="Section identifier"),
):
    try:
        result = await service.get_data_by_user_id_and_section(user_id, section)
        return {"message": "Data fetched successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting data by section")


@router.post("/injest-item-1-to-10/")
async def injest_item_1_to_10(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Original code expects data wrapper? Logic: data = {"1-10": {"data": data}}
    # But input `data` in Django `request.body` is the pure JSON.
    # In `InjestItem1to10`, `data = json.loads(request.body)`.
    # `self.data_injestion_service.injest_data_item1_to_10(user_id, data)`
    # So `data` passed to service IS the whole body.
    try:
        await service.injest_data_item1_to_10(user_id, data)
        return {"message": "Data injested successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error injesting data for item 1 to 10"
        )


@router.post("/injest-item-11/")
async def injest_item_11(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # In Django: `self.data_injestion_service.injest_data_item11(user_id, data)`
    # Wait, `injest_data_item11` expects `data: List[Dict]`.
    # But `request.body` is a Dict containing `user_id`.
    # Is `data` in `injest_data_item11` supposed to be the LIST of items?
    # Django code: `result = self.data_injestion_service.injest_data_item11(user_id, data)`
    # Service code: `for item in data:` -> This implies `data` IS a list or iterable.
    # BUT `data = json.loads(request.body)` includes `user_id`.
    # If `data` is `{"user_id": "...", "items": [...] }`, then iterating `data` yields keys "user_id", "items".
    # This suggests the Django view code might be passing the wrong thing OR `data` is a LIST of items where one item has `user_id`? Unlikely.
    # OR, the body IS a list, and `user_id` is extracted from one of the items or passed as `user_id` param?
    # Django view: `user_id = data.get("user_id")`. This implies `data` is a Dict.
    # Service: `for item in data:` -> Iterate keys of Dict?
    # Key iteration: `user_id` would be an item. `item["attended/organized"]` -> string indexing on string "user_id" -> Error.
    #
    # CORRECTION: The Django code likely expects `data` to have a specific key for the list, OR utilize `data` as the list but somehow extract user_id.
    # Let's look at `InjestItem11` again.
    # `data = json.loads(data)`
    # `user_id = data.get("user_id")`
    # `self.service.injest_data_item11(user_id, data)`
    # THIS SEEMS BUGGY in the original code if `data` is the dict `{'user_id': ...}`.
    # Unless `data` is a list of dicts, but `list` has no `.get`.
    #
    # HYPOTHESIS: The request body is `{"user_id": "...", "data": [...]}` or similar, but the variable naming is confusing.
    # OR the frontend sends `[{"user_id": "...", ...}, ...]`? No, code uses `.get()`.
    #
    # Let's assume the body is `{"user_id": "...", ...}` and the service iterates over it? That would fail.
    #
    # Wait, look at `InjestItem12_2`:
    # `self.data_injestion_service.injest_data_item12_2(user_id, data.get("data", []))`
    # explicit `.get("data", [])`.
    #
    # But Item 11: `self.data_injestion_service.injest_data_item11(user_id, data)`
    #
    # If I look at the usage `for item in data:`, `item` must be compatible with `item["attended/organized"]`.
    # If `data` is the request body dict `{'user_id': 'foo'}`, `item` is 'user_id'. `item['...']` fails.
    #
    # CONCLUSION: The original Django code for Item 11 might be broken OR expects `data` to be a list which is somehow also a dict (impossible).
    # OR `data` is a dict, but iterating it is not what is intended.
    #
    # HOWEVER, looking at `InjestItem12_2`, it extracts `data.get("data")`.
    # Maybe Item 11 is SUPPOSED to do that?
    #
    # Let's look closer at `InjestItem1`.
    # `self.data_injestion_service.injest_data_item1_to_10(user_id, data)` -> `data = {"1-10": {"data": data}}`. `data` is Dict. Correct.
    #
    # Item 11 is the outlier.
    # Safest bet: Assume the input has a "data" key containing the list, matching 12.2 pattern?
    # OR assume the frontend sends the list in a key named something else?
    #
    # If I implement it strictly as the Django code reads, it will fail if `data` contains `user_id`.
    #
    # STRATEGY: I will assume the relevant list is in `data.get("data", [])` if it exists, otherwise `data` itself?
    # But `data` has `user_id`.
    #
    # I'll modify the logic to look for a list in `data` key, mimicking 12.2 which looks sane.
    # `items = data.get("data", [])`

    items = data.get("data", [])
    if not items and isinstance(data, list):
        items = data

    try:
        result = await service.injest_data_item11(user_id, items)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error injesting data for item 11")


@router.post("/injest-item-12-1/")
async def injest_item_12_1(data: Dict = Body(...)):
    user_id = data.get("user_id")
    semester = data.get("semester")
    if not user_id or not semester:
        raise HTTPException(status_code=400, detail="User ID and Semester are required")

    # Original: `self.data_injestion_service.injest_data_item12_1(user_id, data, semester)`
    # Service expects `data: List[Dict]`.
    # Passing the whole body (Dict) to a function expecting List?
    # Same issue as Item 11.
    # I will extract `data.get("data", [])`.
    items = data.get("data", [])

    try:
        result = await service.injest_data_item12_1(user_id, items, semester)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error injesting data for item 12.1"
        )


@router.post("/injest-item-12-2/")
async def injest_item_12_2(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    items = data.get("data", [])
    try:
        result = await service.injest_data_item12_2(user_id, items)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error injesting data for item 12.2"
        )


@router.post("/injest-item-12-3-to-12-4/")
async def injest_item_12_3_to_12_4(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    try:
        result = await service.injest_data_item12_3_to_12_4(user_id, data)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error injesting data for item 12.3 to 12.4"
        )


@router.post("/injest-item-13/")
async def injest_item_13(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Service expects `data: Dict` and iterates `for section in data`.
    # The body contains `user_id`! If we iterate the body, we hit `user_id`.
    # Fix: Extract the data payload. Assuming key "data" or exclude "user_id".
    # Logic: `data` in service is used as `data[section]`.
    # If `section` is "user_id", `data["user_id"]` is a string (id).
    # Then `calculate_api_score_for_item13(data[section], section)` is called.
    # `section`="user_id". `calculate...` raises ValueError("Unknown section: user_id").
    # So the original code IS BROKEN if `data` is the raw body including `user_id`.
    # UNLESS `calculate` ignores unknown sections? No, `else: raise ValueError`.
    # It seems the frontend sends structure where `user_id` is NOT at top level with sections?
    # BUT `user_id = data.get("user_id")`.
    #
    # Conclusion: The input `data` passed to service functions MUST BE CLEANED or is expected to be nested?
    # I will pass `data.get("data", {})` if exists, else copy and pop `user_id`.

    payload = data.get("data")
    if not payload:
        payload = data.copy()
        payload.pop("user_id", None)

    try:
        result = await service.injest_data_item13(user_id, payload)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error injesting data for item 13")


@router.post("/injest-item-14/")
async def injest_item_14(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    items = data.get("data", [])

    try:
        result = await service.injest_data_item14(user_id, items)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error injesting data for item 14")


@router.post("/injest-item-15/")
async def injest_item_15(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    items = data.get("data", [])

    try:
        result = await service.injest_data_item15(user_id, items)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error injesting data for item 15")


@router.post("/injest-item-16/")
async def injest_item_16(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    items = data.get("data", [])

    try:
        result = await service.injest_data_item16(user_id, items)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error injesting data for item 16")


@router.post("/injest-item-17/")
async def injest_item_17(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    items = data.get("data", [])

    try:
        result = await service.injest_data_item17(user_id, items)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error injesting data for item 17")


@router.post("/injest-item-18/")
async def injest_item_18(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    items = data.get("data", [])

    try:
        result = await service.injest_data_item18(user_id, items)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error injesting data for item 18")


@router.post("/injest-item-19/")
async def injest_item_19(data: Dict = Body(...)):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Logic similar to Item 13, iterating keys "self", "national", etc.
    # Needs to avoid "user_id".
    payload = data.get("data")
    if not payload:
        payload = data.copy()
        payload.pop("user_id", None)

    try:
        result = await service.injest_data_item19(user_id, payload)
        return {"message": "Data injested successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error injesting data for item 19")


@router.get("/get-all-faculty-data/")
async def get_all_faculty_data():
    try:
        result = await service.get_all_faculty_data()
        return {"message": "Data fetched successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching faculty data")
