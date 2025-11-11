from backend.services.text_service import query_groq_text
from backend.services.vision_service import query_groq_image

from backend.agents import (
    crop_agent,
    pest_agent,
    irrigation_agent,
    subsidy_agent,
    yield_agent
)

def route_query(query: str = None, image_path: str = None):
    q = (query or "").lower()

    # If image provided → pest detection
    if image_path:
        return pest_agent.handle_query(image_path=image_path)

    #  Pest / disease
    elif any(k in q for k in ["pest", "disease", "leaf", "infection", "spots"]):
        return pest_agent.handle_query(query)

    #  Irrigation / watering
    elif any(k in q for k in ["water", "irrigation", "moisture", "drip"]):
        return irrigation_agent.handle_query(query)

    #  Yield / harvest
    elif any(k in q for k in ["yield", "harvest", "production", "output"]):
        return yield_agent.handle_query(query)

    # Subsidy / scheme
    elif any(k in q for k in ["subsidy", "scheme", "loan", "grant"]):
        return subsidy_agent.handle_query(query)

    #  Default → crop guidance
    else:
        return crop_agent.handle_query(query)
