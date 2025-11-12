"""
master_agent.py
---------------
Central orchestrator for routing user queries to the appropriate AgriGPT agent.
Supports both text and image inputs, and ensures final responses are
cleaned and standardized using the FormatterAgent.
"""

from backend.agents import (
    crop_agent,
    pest_agent,
    irrigation_agent,
    subsidy_agent,
    yield_agent,
    formatter_agent,
)
from backend.services.text_service import query_groq_text

# Initialize agents once (singleton-style reuse)
crop = crop_agent.CropAgent()
pest = pest_agent.PestAgent()
irrigation = irrigation_agent.IrrigationAgent()
subsidy = subsidy_agent.SubsidyAgent()
yield_ = yield_agent.YieldAgent()
formatter = formatter_agent.FormatterAgent()


def route_query(query: str = None, image_path: str = None) -> str:
    """
    Routes the user’s input (text, image, or both) to the appropriate AgriGPT agent.

    Args:
        query (str, optional): The user's text query (e.g., "how to improve yield?")
        image_path (str, optional): The path of an uploaded crop image.

    Returns:
        str: Final formatted response from the relevant AgriGPT agent.
    """
    q = (query or "").lower().strip()

    #  Case 1: Combined Image + Text → Dual Reasoning
    if image_path and query:
        # Step 1: Analyze image using PestAgent
        pest_insight = pest.handle_query(image_path=image_path)

        # Step 2: Contextual reasoning from text (decide agent)
        if any(k in q for k in ["water", "irrigation", "moisture", "drip", "rain"]):
            context = irrigation.handle_query(query)
        elif any(k in q for k in ["yield", "harvest", "production", "output", "productivity"]):
            context = yield_.handle_query(query)
        elif any(k in q for k in ["subsidy", "scheme", "loan", "grant", "support", "fund"]):
            context = subsidy.handle_query(query)
        else:
            context = crop.handle_query(query)

        # Step 3: Merge image and text findings into one coherent answer
        combined_prompt = f"""
        You are AgriGPT, a multimodal agricultural expert.

        The farmer uploaded an image and asked:
        "{query}"

        Visual analysis of the image shows:
        {pest_insight}

        Contextual advice from the text query:
        {context}

        Combine these findings into one clear, actionable response.
        Keep it short, structured, and farmer-friendly.
        """

        combined_response = query_groq_text(combined_prompt)
        return formatter.handle_query(combined_response)

    #  Case 2: Image-only input → Pest/Disease Detection
    if image_path:
        response = pest.handle_query(image_path=image_path)
        return formatter.handle_query(response)

    #  Case 3: Text-only routing
    if not query:
        return "Please provide a query or an image for analysis."

    #  Pest / disease-related
    if any(k in q for k in ["pest", "disease", "leaf", "infection", "spots", "bug", "insect"]):
        response = pest.handle_query(query)

    #  Irrigation / water management
    elif any(k in q for k in ["water", "irrigation", "moisture", "drip", "rain", "sprinkler"]):
        response = irrigation.handle_query(query)

    # Yield / harvest optimization
    elif any(k in q for k in ["yield", "harvest", "production", "output", "productivity"]):
        response = yield_.handle_query(query)

    #  Subsidy / government schemes
    elif any(k in q for k in ["subsidy", "scheme", "loan", "grant", "support", "fund"]):
        response = subsidy.handle_query(query)

    #  Default fallback → Crop guidance
    else:
        response = crop.handle_query(query)

    #  Final Step: Clean and format output
    return formatter.handle_query(response)
