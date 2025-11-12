from backend.services.text_service import query_groq_text
from backend.agents.agri_agent_base import AgriAgentBase


class CropAgent(AgriAgentBase):
    """Agent for providing crop management and cultivation guidance."""

    name = "CropAgent"

    def handle_query(self, query: str = None, image_path: str = None) -> str:
        """
        Handles user queries related to crop advice (fertilizer, soil, timing, yield).
        This agent focuses on actionable, concise, farmer-friendly recommendations.
        """

        if not query:
            response = "Please provide a crop-related question (e.g., 'How to improve rice yield?')."
            return self.respond_and_record("No query provided", response)

        prompt = f"""
        You are AgriGPT, an expert agriculture assistant.
        The user asked: "{query}"

        Provide clear, practical crop advice covering:
        - Fertilizer use and dosage
        - Soil preparation and nutrients
        - Crop growth timing or yield improvement tips
        Keep your tone short, supportive, and farmer-friendly.
        """

        # Query Groq model for text response
        response = query_groq_text(prompt)

        # Log and return
        return self.respond_and_record(query, response, query_type="text")
