from fastapi import APIRouter, UploadFile, File
import tempfile
from backend.agents.master_agent import route_query

router = APIRouter(prefix="/analyze", tags=["Image Analysis"])

@router.post("/")
async def analyze_image(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    response = route_query(query=None, image_path=tmp_path)
    return {"analysis": response}
