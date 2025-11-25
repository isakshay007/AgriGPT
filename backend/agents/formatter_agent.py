# backend/agents/formatter_agent.py

from backend.services.text_service import query_groq_text
from backend.agents.agri_agent_base import AgriAgentBase


class FormatterAgent(AgriAgentBase):
    name = "FormatterAgent"

    def handle_query(self, query: str = None, image_path: str = None) -> str:
        """
        Formatter agent:
        - Cleans & beautifies final answers
        - Adds a simple title, bullets, short lines
        - ALWAYS returns safe string output
        """

        # Normalize text (consistent with all other agents)
        if not query or not isinstance(query, str) or not query.strip():
            msg = "No text was provided for formatting."
            return self.respond_and_record(query or "", msg, image_path)

        clean_query = query.strip()

        # Formatting prompt
        prompt = f"""
        You are AgriGPT Formatter.

        Reformat the following content to make it
        clearer, structured, and farmer-friendly:

        \"\"\"{clean_query}\"\"\"

        Formatting Rules:
        - Add a short 3–6 word title
        - Use clear bullet points
        - Short, simple sentences
        - Farmer-friendly tone
        - End with a 1-line summary
        - Remove repetition and fluff
        """

        # Query Groq safely
        try:
            formatted = query_groq_text(prompt)
        except Exception as e:
            formatted = f"Error formatting text: {e}"

        # Ensure ALWAYS a string
        formatted = str(formatted)

        return self.respond_and_record(clean_query, formatted, image_path)
