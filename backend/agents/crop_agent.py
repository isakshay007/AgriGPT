from backend.services.text_service import query_groq_text

def handle_query(query: str):
    prompt = f"""
    You are AgriGPT, an AI agriculture advisor.
    The user asked: "{query}"
    Provide clear, practical crop advice — covering fertilizer, soil, timing, or yield tips.
    Keep your tone short and farmer-friendly.
    """
    return query_groq_text(prompt)
