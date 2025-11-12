from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from backend.services.history_service import log_interaction

class AgriAgentBase(ABC):
    """
    Base class for all AgriGPT agents.
    Defines a consistent interface for handling text or image queries
    and logging their responses for tracking and analysis.
    """

    name: str = "AgriAgentBase"


    # Abstract method — must be implemented by each agent

    @abstractmethod
    def handle_query(self, query: Optional[str] = None, image_path: Optional[str] = None) -> str:
        """
        Process a user query (text, image, or both) and return the model's response.
        Each derived agent (e.g., PestAgent, IrrigationAgent) implements this logic.
        """
        pass

    # Log an interaction for traceability

    def record(self, query: str, response: str, query_type: str = "text") -> None:
        """
        Save a structured log entry of the agent's interaction.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.name,
            "query": query,
            "response": response,
            "type": query_type
        }
        log_interaction(entry)

    # Helper for subclasses: return + log in one step
    def respond_and_record(self, query: str, response: str, query_type: str = "text") -> str:
        """
        Return a response and record it automatically.
        Used by derived agents to keep code clean and consistent.
        """
        self.record(query, response, query_type)
        return response
