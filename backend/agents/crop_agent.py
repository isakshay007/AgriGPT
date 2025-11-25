# backend/agents/crop_agent.py

from backend.services.text_service import query_groq_text
from backend.agents.agri_agent_base import AgriAgentBase


class CropAgent(AgriAgentBase):
    """Provides general crop management, fertilizer, soil, and cultivation advice."""

    name = "CropAgent"

    def handle_query(self, query: str = None, image_path: str = None) -> str:
        """
        Handles crop-related text questions:
        - Fertilizer dosage
        - Soil preparation
        - Crop growth timing
        - Yield improvement
        """

        # Normalize text
        if not query or not query.strip():
            response = (
                "Please ask a crop-related question. Example:\n"
                "- How to improve my rice yield?\n"
                "- What fertilizer should I use for tomatoes?"
            )
            return self.respond_and_record(
                query="",
                response=response,
                image_path=image_path
            )

        clean_query = query.strip()

        # Build LLM prompt
        prompt = f"""
        You are AgriGPT – Crop Management Specialist.

        The farmer asks:
        "{clean_query}"

        Provide clear, simple, farmer-friendly advice.
        Include:
        • Fertilizer type + dosage
        • Soil preparation steps
        • Growth-stage guidance or yield improvement tips
        • 3–5 specific actionable steps (no theory)
        • Tamil Nadu / Kharif seasonal context where relevant

        Keep the answer practical and easy to follow.
        """

        # Query Groq (always returns string through base class)
        try:
            resp = query_groq_text(prompt)
        except Exception as e:
            resp = f"Error generating crop advice: {e}"

        # Log + return (respond_and_record always enforces string)
        return self.respond_and_record(
            query=clean_query,
            response=resp,
            image_path=image_path
        )
