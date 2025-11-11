from backend.services.text_service import query_groq_text

def handle_query(query: str):
    """
    Handles queries related to agricultural subsidies, government schemes, and financial assistance.

    Example:
    - "What are the subsidies for drip irrigation?"
    - "Tell me about government schemes for farmers in Tamil Nadu."
    """
    prompt = f"""
    You are AgriGPT, an intelligent assistant for Indian farmers.

    The user asked: "{query}"

    Provide concise, up-to-date information about relevant agricultural subsidies, 
    schemes, or loans available to farmers. 
    If applicable, include central or state-level government programs.

    Format the response in clear, farmer-friendly language.
    """

    return query_groq_text(prompt)
