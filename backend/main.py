from fastapi import FastAPI
from backend.routes import query_router, image_router

app = FastAPI(title="AgriGPT Backend (Groq + LLaMA-4 Scout)")

app.include_router(query_router.router)
app.include_router(image_router.router)

@app.get("/")
def root():
    return {"message": "AgriGPT Backend running with Groq API 🚀"}
