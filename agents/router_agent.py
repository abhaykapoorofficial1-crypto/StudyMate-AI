from agents.base_agent import BaseAgent
from agents.explain_agent import explain_agent
from agents.quiz_agent import quiz_agent
from agents.notes_agent import notes_agent
from agents.planner_agent import planner_agent
from agents.flashcard_agent import flashcard_agent
from agents.progress_agent import progress_agent
from agents.memory_agent import memory_agent
from security.logging import logger

class RouterAgent(BaseAgent):
    """
    Master Orchestrator Agent under Google ADK architecture.
    Analyzes user intent and delegates execution to specialized sub-agents.
    """

    def __init__(self):
        super().__init__(
            name="RouterAgent",
            description="Master intent classifier and task delegator routing user requests to specialized domain agents."
        )
        self.agents = {
            "explain": explain_agent,
            "quiz": quiz_agent,
            "notes": notes_agent,
            "planner": planner_agent,
            "flashcard": flashcard_agent,
            "progress": progress_agent,
            "memory": memory_agent
        }

    def route_and_process(self, user_prompt: str, context: dict = None) -> str:
        """Determines intent and routes to appropriate sub-agent."""
        prompt_lower = user_prompt.lower()

        target_agent = explain_agent # default fallback

        if any(k in prompt_lower for k in ["quiz", "mcq", "test", "question", "true/false", "fill in"]):
            target_agent = quiz_agent
        elif any(k in prompt_lower for k in ["note", "summary", "summarize", "bullet", "formula", "mind map"]):
            target_agent = notes_agent
        elif any(k in prompt_lower for k in ["plan", "schedule", "timetable", "countdown", "exam"]):
            target_agent = planner_agent
        elif any(k in prompt_lower for k in ["flashcard", "card", "deck"]):
            target_agent = flashcard_agent
        elif any(k in prompt_lower for k in ["progress", "stats", "streak", "badge", "dashboard", "metric", "weak"]):
            target_agent = progress_agent
        elif any(k in prompt_lower for k in ["history", "memory", "recent", "document list"]):
            target_agent = memory_agent

        logger.info(f"ROUTER AGENT: Delegating prompt '{user_prompt[:50]}...' to target '{target_agent.name}'")
        return target_agent.process_request(user_prompt, context)

    def _generate_fallback(self, prompt: str, context: dict = None) -> str:
        return self.route_and_process(prompt, context)

router_agent = RouterAgent()
