from backend.services.text_service import query_groq_text
from backend.services.vision_service import query_groq_image
from backend.agents.agri_agent_base import AgriAgentBase


class PestAgent(AgriAgentBase):
    """
    AgriGPT Pest & Disease Agent
    -----------------------------
    Detects crop pests or diseases using text or image analysis.
    Suggests likely causes, visible symptoms, and simple organic or
    chemical treatments with preventive guidance.
    """

    name = "PestAgent"

    def handle_query(self, query: str = None, image_path: str = None) -> str:
        """
        Handles pest and disease detection requests.

        - If an image is provided → runs image-based analysis.
        - If only text is provided → interprets user description.
        """

        #  Fallback: no input
        if not query and not image_path:
            response = (
                "Please provide a crop image or describe the symptoms "
                "(e.g., yellow leaves, black spots, or pest damage) "
                "so I can help identify the issue."
            )
            return self.respond_and_record("No input provided", response, query_type="text")

        #  Case 1: Image-based pest or disease detection
        if image_path:
            prompt = """
            Analyze this crop image and identify any visible pests, diseases, or nutrient deficiencies.
            Describe:
            - The likely problem or pest name
            - Visual indicators or symptoms
            - Recommended treatments (organic or chemical)
            - Preventive measures to avoid recurrence

            Keep the explanation simple and actionable for farmers.
            """
            response = query_groq_image(image_path, prompt)
            return self.respond_and_record("Image-based pest analysis", response, query_type="image")

        #  Case 2: Text-based pest diagnosis
        else:
            prompt = f"""
            You are AgriGPT, an intelligent pest and disease diagnosis assistant.

            The user described: "{query}"

            Based on this description, identify the most likely pest, infection, or deficiency.
            Include:
            - The probable cause or pest name
            - Key visible symptoms
            - Recommended treatments (organic and chemical)
            - Preventive care and maintenance tips

            Keep the response short, clear, and written in a farmer-friendly way.
            """
            response = query_groq_text(prompt)
            return self.respond_and_record(query, response, query_type="text")
