# backend/agents/yield_agent.py

from backend.services.text_service import query_groq_text
from backend.agents.agri_agent_base import AgriAgentBase


class YieldAgent(AgriAgentBase):
    """
    Yield Optimization Agent
    ------------------------
    Gives farmers:
    - Expected yield range for a crop
    - Root causes for low yield
    - Stage-wise improvement plan
    - Simple, practical recommendations
    """

    name = "YieldAgent"

    def handle_query(self, query: str = None, image_path: str = None) -> str:
        """
        Handles all yield-related questions.
        Image input is ignored for this agent.
        """

        # ------------------------------------------------------
        # CASE 0 — Empty or missing text
        # ------------------------------------------------------
        if not query or not query.strip():
            msg = (
                "Please describe your crop and the yield problem. Examples:\n"
                "- 'My rice yield is low this season'\n"
                "- 'Maize giving only 2 tons per hectare'\n"
                "- 'Tomato plants producing fewer fruits'\n"
            )
            return self.respond_and_record(
                query="No query provided",
                response=msg,
                image_path=image_path
            )

        query_clean = query.strip()

        # ------------------------------------------------------
        # CASE 1 — Build LLM prompt
        # ------------------------------------------------------
        prompt = f"""
        You are **AgriGPT – Yield Improvement Advisor**.

        The farmer asks:
        \"\"\"{query_clean}\"\"\"

        Provide clear guidance with:

        **1. Expected Yield Range**
        - Typical India/global yield range for this crop.

        **2. Causes of Low Yield**
        Cover major factors:
        - Soil nutrient imbalance
        - Fertilizer schedule mistakes
        - Water stress (too much or too little)
        - Pests or diseases affecting yield
        - Poor seed variety
        - Climate or incorrect planting time

        **3. Practical Improvement Steps**
        Include:
        - Ideal fertilizer schedule (stage-wise)
        - Correct irrigation intervals
        - Soil enrichment methods
        - Pest/disease prevention tips
        - Recommended varieties for better yield

        **4. Language Style**
        - Short bullet points
        - Simple Indian farmer-friendly tone
        - No technical jargon
        - Clear, step-by-step format
        """

        # ------------------------------------------------------
        # CASE 2 — Query Groq Safely
        # ------------------------------------------------------
        try:
            output = query_groq_text(prompt)
        except Exception as e:
            output = f"Error generating yield advice: {str(e)}"

        # ------------------------------------------------------
        # CASE 3 — Log + Return
        # ------------------------------------------------------
        return self.respond_and_record(
            query=query_clean,
            response=output,
            image_path=image_path
        )
