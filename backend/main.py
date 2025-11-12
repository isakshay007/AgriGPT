from fastapi import FastAPI
from backend.routes import ask_router, health_router

app = FastAPI(
    title="AgriGPT Backend (Groq + LLaMA-4 Scout)",
    description="Unified multimodal backend for AgriGPT — handles both text and image queries.",
    version="1.0.0",
)

app.include_router(ask_router.router)
app.include_router(health_router.router)

@app.get("/")
def root():
    """Root endpoint for quick API check."""
    return {
        "message": "🌾 AgriGPT Backend running successfully with Groq API and unified multimodal query endpoint 🚀",
        "available_endpoints": ["/ask", "/health", "/docs"]
    }
