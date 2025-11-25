# backend/agents/subsidy_agent.py

from backend.services.text_service import query_groq_text
from backend.agents.agri_agent_base import AgriAgentBase
from backend.services.rag_service import rag_service
import unicodedata


class SubsidyAgent(AgriAgentBase):
    """Subsidy & Government Scheme Agent"""

    name = "SubsidyAgent"

    def _sanitize_query(self, text: str) -> str:
        if not text:
            return ""
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("\x00", "").replace("\u200c", "")
        return text.strip()

    def handle_query(self, query: str = None, image_path: str = None) -> str:
        if not query or not query.strip():
            msg = (
                "Please ask about a specific subsidy or government scheme:\n"
                "- 'Drip irrigation subsidy in Tamil Nadu'\n"
                "- 'PM-Kisan eligibility'\n"
            )
            return self.respond_and_record("", msg, image_path)

        query_clean = self._sanitize_query(query)
        context_str = ""

        try:
            # ✅ Now returns List[Dict] - safe for OpenAPI
            retrieved_docs = rag_service.retrieve(query_clean)
            
            if retrieved_docs:
                context_str += "\n\n**Retrieved Official Information:**\n"
                for i, doc in enumerate(retrieved_docs, 1):
                    # ✅ Dict access (not Pydantic)
                    context_str += (
                        f"Scheme {i}: {doc['scheme_name']}\n"
                        f"- Eligibility: {doc['eligibility']}\n"
                        f"- Benefits: {doc['benefits']}\n"
                        f"- Application: {doc['application_steps']}\n"
                        f"- Documents: {doc['documents']}\n"
                        f"- Notes: {doc['notes']}\n\n"
                    )
            else:
                context_str += "\n\n(No official scheme found.)\n"
                
        except Exception as e:
            context_str += f"\n\n[RAG ERROR] {str(e)}\n"

        prompt = f"""
        You are AgriGPT, expert on Indian agricultural subsidies.

        Farmer asked: "{query_clean}"

        {context_str}

        Provide:
        1. Scheme name
        2. Government level
        3. Eligibility
        4. Benefits
        5. Application process

        Use bullet points and simple language.
        """

        try:
            result = query_groq_text(prompt)
        except Exception as e:
            result = f"Error: {e}"

        return self.respond_and_record(query_clean, result, image_path)