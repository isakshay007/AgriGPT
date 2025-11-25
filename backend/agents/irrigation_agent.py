# backend/agents/irrigation_agent.py

from backend.services.text_service import query_groq_text
from backend.agents.agri_agent_base import AgriAgentBase


class IrrigationAgent(AgriAgentBase):
    """
    Irrigation Agent
    -----------------
    Provides guidance on:
    - Watering intervals
    - Soil moisture balance
    - Drip/sprinkler use
    - Water-saving methods
    """

    name = "IrrigationAgent"

    def handle_query(self, query: str = None, image_path: str = None) -> str:
        """
        Irrigation logic.
        Image input is ignored for this agent.
        """

        # ------------------------------------------------------
        # CASE 0 — Validate query
        # ------------------------------------------------------
        if not query or not isinstance(query, str) or not query.strip():
            msg = (
                "Please ask an irrigation-related question such as:\n"
                "- 'How often should I irrigate onions?'\n"
                "- 'How to save water in drip irrigation?'\n"
                "- 'How to adjust irrigation during summer?'\n"
            )
            return self.respond_and_record(
                query or "",
                msg,
                image_path=image_path,
            )

        query_clean = query.strip()

        # ------------------------------------------------------
        # CASE 1 — Construct robust prompt
        # ------------------------------------------------------
        prompt = f"""
        You are **AgriGPT – Irrigation Expert**.

        The farmer asked:
        \"{query_clean}\"

        Provide clear irrigation guidance covering:
        - Correct watering intervals (daily / weekly / stage-based)
        - Soil moisture checking & maintenance
        - Drip, sprinkler, and flood irrigation best practices
        - Water-saving techniques (mulching, scheduling, pressure control)
        - Adjusting irrigation during rainfall or extreme heat
        - Soil-type adjustments (sandy, clay, loam)

        Use:
        - Bullet points
        - Short sentences
        - Very farmer-friendly tone
        """

        # ------------------------------------------------------
        # CASE 2 — Query Groq safely
        # ------------------------------------------------------
        try:
            result = query_groq_text(prompt)
        except Exception as e:
            result = f"Error generating irrigation advice: {e}"

        # Always safe-string
        result = str(result)

        # ------------------------------------------------------
        # CASE 3 — Log & Return
        # ------------------------------------------------------
        return self.respond_and_record(
            query_clean,
            result,
            image_path=image_path,
        )
