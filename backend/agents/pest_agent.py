from backend.services.text_service import query_groq_text
from backend.services.vision_service import query_groq_image

def handle_query(query: str = None, image_path: str = None):
    if image_path:
        prompt = "Analyze this crop image and identify any visible pests or diseases."
        return query_groq_image(image_path, prompt)
    else:
        prompt = f"The user reported: '{query}'. Identify likely pest or disease and suggest treatment steps."
        return query_groq_text(prompt)
