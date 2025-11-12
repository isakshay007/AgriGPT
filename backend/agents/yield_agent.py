from backend.services.text_service import query_groq_text
from backend.agents.agri_agent_base import AgriAgentBase


class YieldAgent(AgriAgentBase):
    """
    Provides crop yield forecasting and productivity optimization tips.
    Helps farmers identify key factors affecting yield and offers practical
    recommendations to maximize output.
    """

    name = "YieldAgent"

    def handle_query(self, query: str = None, image_path: str = None) -> str:
        """
        Handles yield-related queries from farmers.

        Example queries:
        - "How can I increase my wheat yield?"
        - "What affects rice yield during monsoon season?"
        - "Why is my corn yield decreasing?"

        Returns:
            A concise, farmer-friendly explanation including trends,
            influencing factors, and actionable yield improvement advice.
        """

        #  Handle missing or empty query
        if not query:
            response = "Please provide details about your crop and the issue you're facing to estimate or improve yield."
            return self.respond_and_record("No query provided", response)

        # Construct Groq text prompt
        prompt = f"""
        You are AgriGPT, an expert crop yield optimization assistant.

        The user asked: "{query}"

        Provide a clear, practical response that includes:
        - Current or expected yield trends
        - Key factors influencing yield (soil, fertilizer, irrigation, pest control)
        - Actionable steps to improve productivity
        - Simple explanations a farmer can easily follow

        Keep the tone short, positive, and farmer-friendly.
        """

        # Generate and log the AI response
        response = query_groq_text(prompt)
        return self.respond_and_record(query, response, query_type="text")
