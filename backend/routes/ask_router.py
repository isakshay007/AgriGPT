from fastapi import (
    APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
)
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tempfile, os, time, uuid
from typing import Optional
from backend.agents.master_agent import route_query

router = APIRouter(prefix="/ask", tags=["Unified Multimodal Query"])

ALLOWED_IMAGE_MIME = {"image/jpeg", "image/png"}
MAX_UPLOAD_BYTES = 8 * 1024 * 1024  # 8 MB


# ✅ Schema for consistent response in Swagger
class AskResponse(BaseModel):
    request_id: str
    status: str
    elapsed_ms: int
    input: dict
    analysis: str


# ----------------------------------------------------
# 1️⃣ TEXT-ONLY ENDPOINT
# ----------------------------------------------------
@router.post("/text", response_model=AskResponse, response_class=JSONResponse)
async def ask_text(
    query: str = Form(..., description="Enter your agricultural question (e.g., 'How to improve rice yield?')")
):
    """
    Handles text-only queries (no image).
    """
    start = time.time()
    request_id = str(uuid.uuid4())

    if not query.strip():
        raise HTTPException(status_code=400, detail="Please provide a valid text query.")

    response = route_query(query=query, image_path=None)

    return {
        "request_id": request_id,
        "status": "success",
        "elapsed_ms": int((time.time() - start) * 1000),
        "input": {"query": query, "image_uploaded": False},
        "analysis": response
    }


# ----------------------------------------------------
# 2️⃣ IMAGE-ONLY ENDPOINT
# ----------------------------------------------------
@router.post("/image", response_model=AskResponse, response_class=JSONResponse)
async def ask_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Upload an image of your crop (JPEG/PNG only).")
):
    """
    Handles image-only queries (pest or disease detection).
    """
    start = time.time()
    request_id = str(uuid.uuid4())
    tmp_path = None

    try:
        if file.content_type not in ALLOWED_IMAGE_MIME:
            raise HTTPException(status_code=415, detail="Unsupported image type.")
        data = await file.read()
        if not data:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        if len(data) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="File too large (max 8MB).")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        response = route_query(query=None, image_path=tmp_path)

        background_tasks.add_task(os.remove, tmp_path)

        return {
            "request_id": request_id,
            "status": "success",
            "elapsed_ms": int((time.time() - start) * 1000),
            "input": {"query": "No text provided", "image_uploaded": True},
            "analysis": response
        }

    except Exception as e:
        if tmp_path and os.path.exists(tmp_path):
            background_tasks.add_task(os.remove, tmp_path)
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")
