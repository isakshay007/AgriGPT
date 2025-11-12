from backend.services.text_service import query_groq_text
from backend.agents.agri_agent_base import AgriAgentBase


class FormatterAgent(AgriAgentBase):
    """
    AgriGPT Formatter Agent
    -----------------------
    Refines and cleans responses from other agents.
    Ensures that outputs are concise, structured, and easy
    to read for farmers or display in the frontend.
    """

    name = "FormatterAgent"

    def handle_query(self, text: str = None, image_path: str = None) -> str:
        """
        Takes raw text from other AgriGPT agents and reformats it
        into short, clear, and farmer-friendly guidance.

        Example usage:
        - Called automatically by `master_agent` after main agent responses.
        - Can also be used directly to refine or standardize text outputs.
        """

        # Handle missing text
        if not text:
            response = "No text was provided for formatting."
            return self.respond_and_record("Empty input", response)

        #  Construct Groq formatting prompt
        prompt = f"""
        You are AgriGPT’s Formatter Assistant.

        Your task is to clean, simplify, and reformat the following farming advice:

        {text}

        Please:
        - Add a clear, short title (3–6 words)
        - Use bullet points for clarity
        - Keep sentences short and action-focused
        - Include a one-line summary at the end
        - Remove redundancy, formal tone, or complex phrasing

        Keep the tone simple, supportive, and easy for farmers to read on mobile devices.
        """

        # Generate formatted version
        formatted = query_groq_text(prompt)

        # Record and return formatted response
        return self.respond_and_record(text, formatted, query_type="text")
