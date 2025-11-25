"""
Master Agent Router (OPENAPI-SAFE - Pydantic Isolated)
------------------------------------------------------
- Pydantic models are LOCAL only (never exposed to FastAPI)
- Uses get_agent_registry() factory
- All outputs are strings
"""

from __future__ import annotations
from typing import Optional, List, Tuple, Dict, Any

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

from backend.core.langchain_tools import (
    AGENT_DESCRIPTIONS,
    NON_ROUTABLE_AGENTS,
    get_agent_registry,
)
from backend.core.llm_client import get_llm
from backend.services.text_service import query_groq_text

MAX_QUERY_CHARS = 2000


def _get_router_llm():
    """Get fresh LLM instance."""
    return get_llm()


def _format_agent_descriptions() -> str:
    """Format agent descriptions for prompt."""
    lines = []
    for agent in AGENT_DESCRIPTIONS:
        name = str(agent.get("name", ""))
        desc = str(agent.get("description", ""))
        lines.append(f"- {name}: {desc}")
    return "\n".join(lines)


# ============================================================
# MAIN API ENTRYPOINT
# ============================================================

def route_query(query: Optional[str] = None, image_path: Optional[str] = None) -> str:
    """
    Main routing function - returns plain string (OpenAPI-safe).
    """
    registry = get_agent_registry()

    if query is not None:
        query = query.strip() or None

    if query and len(query) > MAX_QUERY_CHARS:
        return f"Query too long (>{MAX_QUERY_CHARS} chars). Please shorten."

    # MULTIMODAL (text + image)
    if image_path and query:
        pest_agent = registry["PestAgent"]
        pest_output = str(pest_agent.handle_query(query=query, image_path=image_path))

        agent_names, _ = _choose_agents_via_llm(query)

        responses = []
        for name in agent_names:
            if name == "PestAgent":
                continue
            agent = registry.get(name)
            if agent:
                responses.append(str(agent.handle_query(query=query)))

        merged = "\n\n---\n\n".join(responses) or "No text-based advice."

        final_prompt = f"""
        You are AgriGPT (Multimodal Expert).
        Farmer question: "{query}"
        Image diagnosis: {pest_output}
        Expert guidance: {merged}
        Provide one clear answer in farmer-friendly language.
        """.strip()

        combined = str(query_groq_text(final_prompt))
        formatter = registry["FormatterAgent"]
        return str(formatter.handle_query(combined))

    # IMAGE ONLY
    if image_path:
        pest_agent = registry["PestAgent"]
        resp = str(pest_agent.handle_query(query="", image_path=image_path))
        formatter = registry["FormatterAgent"]
        return str(formatter.handle_query(resp))

    # NO INPUT
    if not query:
        return "Please provide a text query or image."

    # TEXT ONLY
    return str(_run_text_pipeline(query, registry))


# ============================================================
# TEXT PIPELINE
# ============================================================

def _run_text_pipeline(query: str, registry: Dict[str, Any]) -> str:
    """Process text-only queries."""
    agent_names, reasoning = _choose_agents_via_llm(query)

    outputs = []
    for name in agent_names:
        agent = registry.get(name)
        if agent:
            outputs.append(str(agent.handle_query(query=query)))

    if not outputs:
        outputs.append(str(registry["CropAgent"].handle_query(query=query)))

    merged = "\n\n---\n\n".join(outputs)
    formatter = registry["FormatterAgent"]
    final = str(formatter.handle_query(merged))

    if reasoning:
        final += f"\n\n_(Router: {reasoning})_"

    return final


# ============================================================
# LANGCHAIN ROUTER (PYDANTIC ISOLATED HERE)
# ============================================================

def _build_router_chain() -> RunnableSequence:
    """
    Build semantic router chain.
    ⚠️ Pydantic is LOCAL only - never exposed to FastAPI.
    """
    agent_descriptions = _format_agent_descriptions()

    template = """
You are AgriGPT Router.
Analyze the query and select 1-3 relevant agents.

Available agents:
{agent_descriptions}

Return ONLY valid JSON (no markdown, no code blocks):
{{
    "agents": ["AgentName1", "AgentName2"],
    "reason": "Brief explanation"
}}

Query: {query}
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["query"],
        partial_variables={"agent_descriptions": agent_descriptions}
    )

    # ✅ Use StrOutputParser - no Pydantic in chain
    chain = prompt | _get_router_llm() | StrOutputParser()
    
    return chain


def _choose_agents_via_llm(query: str) -> Tuple[List[str], str]:
    """
    Choose agents using LLM.
    Returns: (agent_names, reason) - plain types only.
    """
    try:
        chain = _build_router_chain()
        raw_output = chain.invoke({"query": query})
        
        # Manual JSON parsing (OpenAPI-safe)
        import json
        import re
        
        # Extract JSON from markdown wrapper if present
        json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {"agents": ["CropAgent"], "reason": "Parse failed"}
        
        # Extract agents
        agents = result.get("agents", [])
        if isinstance(agents, str):
            agents = [agents]
        
        # Filter non-routable agents
        agents = [a for a in agents if a not in NON_ROUTABLE_AGENTS]
        
        reason = str(result.get("reason", ""))
        
        if not agents:
            return ["CropAgent"], "Fallback: no valid agents"
        
        return agents, reason

    except Exception as e:
        return ["CropAgent"], f"Router failed: {str(e)}"