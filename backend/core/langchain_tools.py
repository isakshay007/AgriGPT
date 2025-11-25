"""
OpenAPI-safe langchain_tools.py
--------------------------------
NO global agent instances.
Only pure data objects are allowed globally.
"""

from __future__ import annotations
from typing import Dict, List

# Import agent classes (no instantiation)
from backend.agents.crop_agent import CropAgent
from backend.agents.irrigation_agent import IrrigationAgent
from backend.agents.pest_agent import PestAgent
from backend.agents.subsidy_agent import SubsidyAgent
from backend.agents.yield_agent import YieldAgent
from backend.agents.formatter_agent import FormatterAgent


# ---------------------------------------------------------
# Non-routable agents
# ---------------------------------------------------------
NON_ROUTABLE_AGENTS = {"FormatterAgent"}


# ---------------------------------------------------------
# FACTORY: create clean instances ONLY when needed
# ---------------------------------------------------------
def get_agent_registry() -> Dict[str, object]:
    """
    Return a fresh registry each time.
    No global objects → FastAPI OpenAPI cannot crash.
    """
    return {
        "CropAgent": CropAgent(),
        "PestAgent": PestAgent(),
        "IrrigationAgent": IrrigationAgent(),
        "SubsidyAgent": SubsidyAgent(),
        "YieldAgent": YieldAgent(),
        "FormatterAgent": FormatterAgent(),
    }


# ---------------------------------------------------------
# Pure text descriptions for the router (allowed)
# ---------------------------------------------------------
AGENT_DESCRIPTIONS: List[dict] = [
    {
        "name": "CropAgent",
        "description": (
            "General crop management: fertilizer schedules, soil preparation, "
            "planting techniques, growth stages, and best farming practices."
        ),
    },
    {
        "name": "PestAgent",
        "description": (
            "Pest and disease detection: insects, fungi, leaf spots, larvae, "
            "and nutrient deficiency signs using text or images."
        ),
    },
    {
        "name": "IrrigationAgent",
        "description": (
            "Water management: irrigation intervals, soil moisture problems, "
            "drip/sprinkler guidance, and water-saving techniques."
        ),
    },
    {
        "name": "YieldAgent",
        "description": (
            "Yield optimization: diagnosing low productivity and providing "
            "practical steps to increase harvest output."
        ),
    },
    {
        "name": "SubsidyAgent",
        "description": (
            "Government schemes: subsidies, loans, PM-Kisan, micro-irrigation programs, "
            "and machinery subsidies."
        ),
    },
]
