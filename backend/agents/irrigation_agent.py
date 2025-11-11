

from backend.services.text_service import query_groq_text

def handle_query(query: str):
    prompt = f"""
    You are AgriGPT, an irrigation planning assistant for farmers.
    The user asked: "{query}"

    Provide simple, region-independent irrigation recommendations such as:
    - Optimal watering intervals
    - Soil moisture balance
    - Water-saving tips
    - (If rainfall or weather data available later, mention that)

    Respond concisely and practically.
    """
    return query_groq_text(prompt)
