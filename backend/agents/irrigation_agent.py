from backend.services.text_service import query_groq_text
from backend.agents.agri_agent_base import AgriAgentBase


class IrrigationAgent(AgriAgentBase):
    """
    AgriGPT Irrigation Agent
    ------------------------
    Provides region-independent irrigation planning and water management guidance.
    Suggests optimal watering intervals, soil-moisture balance, and efficient
    water-saving practices tailored for general farm conditions.
    """

    name = "IrrigationAgent"

    def handle_query(self, query: str = None, image_path: str = None) -> str:
        """
        Handles irrigation-related queries and returns concise, practical recommendations.

        Example queries:
        - "How often should I water tomato plants in summer?"
        - "What’s the ideal soil moisture for paddy fields?"
        - "How can I save water using drip irrigation?"
        """

        #  Handle missing or empty query
        if not query:
            response = (
                "Please provide an irrigation-related question, "
                "such as 'How often should I water my crop?' or 'Tips to save water using drip systems.'"
            )
            return self.respond_and_record("No query provided", response)

        #  Construct Groq prompt for irrigation planning
        prompt = f"""
        You are AgriGPT, an expert irrigation planning assistant for farmers.

        The user asked: "{query}"

        Provide region-independent irrigation recommendations that include:
        - Optimal watering intervals (daily, weekly, or based on crop stage)
        - Soil moisture balance guidance (how to check and maintain)
        - Practical water-saving methods (drip irrigation, mulching, scheduling)
        - Mention how rainfall or weather forecasts can optimize watering.

        Keep the response short, supportive, and written in clear farmer-friendly language.
        Use bullet points or compact paragraphs for easy reading.
        """

        # Query Groq model for response
        response = query_groq_text(prompt)

        # Log and return
        return self.respond_and_record(query, response, query_type="text")
