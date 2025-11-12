# backend/routes/health_router.py
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check():
    """Basic health check to confirm the API is running"""
    return {"status": "OK", "message": "AgriGPT backend is alive 🚜"}
