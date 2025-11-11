from fastapi import APIRouter
from backend.agents.master_agent import route_query

router = APIRouter(prefix="/query", tags=["Text Queries"])

@router.post("/")
async def handle_query(payload: dict):
    query = payload.get("query")
    if not query:
        return {"error": "Missing 'query' text"}
    response = route_query(query)
    return {"answer": response}
