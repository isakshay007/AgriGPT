"""
yield_agent.py
---------------
Provides crop yield estimation and optimization tips based on user queries.
Future versions can use region or season data for precise forecasts.
"""

from backend.services.text_service import query_groq_text

def handle_query(query: str):
    prompt = f"""
    You are AgriGPT, an expert on crop yield forecasting and optimization.
    The user asked: "{query}"

    Give a clear answer including:
    - Expected yield trends
    - Key factors that influence yield (soil, fertilizer, irrigation, pest control)
    - Actionable tips to increase productivity
    - Simple explanations a farmer can follow

    Keep it short, friendly, and practical.
    """
    return query_groq_text(prompt)
