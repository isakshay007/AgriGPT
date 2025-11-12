from backend.services.text_service import query_groq_text
from backend.agents.agri_agent_base import AgriAgentBase


class SubsidyAgent(AgriAgentBase):
    """
    AgriGPT Subsidy & Scheme Agent
    ------------------------------
    Provides clear and up-to-date information on Indian agricultural
    subsidies, government schemes, and farmer loan programs.
    """

    name = "SubsidyAgent"

    def handle_query(self, query: str = None, image_path: str = None) -> str:
        """
        Handles queries related to farming subsidies, state/central schemes,
        and financial assistance for farmers.
        """

        #  Handle empty or invalid queries
        if not query:
            response = "Please ask about a specific subsidy, scheme, or loan program (e.g., 'drip irrigation subsidy in Tamil Nadu')."
            return self.respond_and_record("No query provided", response)

        #  Construct smart Groq prompt
        prompt = f"""
        You are AgriGPT, an intelligent assistant for Indian farmers.

        The user asked: "{query}"

        Provide clear and accurate information on relevant agricultural
        subsidies, schemes, or loan programs. Include:
        - The scheme name and purpose
        - Whether it is a Central or State government initiative
        - Basic eligibility or target group
        - Key benefits or financial support available

        Keep the response brief, accurate, and easy for farmers to understand.
        Use bullet points wherever possible.
        """

        # Get Groq-based response and log the result
        response = query_groq_text(prompt)
        return self.respond_and_record(query, response, query_type="text")
