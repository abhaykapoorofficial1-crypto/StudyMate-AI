import time
from abc import ABC, abstractmethod
from config.settings import settings
from security.prompt_guard import prompt_guard
from security.validators import validator
from security.permissions import permission_manager
from security.rate_limit import rate_limiter
from security.logging import logger, log_agent_execution
from memory.sqlite_memory import memory_db

# Try importing google genai SDK
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class BaseAgent(ABC):
    """
    Abstract Base Agent enforcing Google ADK security standards, 
    RBAC permissions, audit logging, and dual online/offline execution pipelines.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.client = None
        
        if HAS_GENAI and settings.gemini_api_key:
            try:
                self.client = genai.Client(api_key=settings.gemini_api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini Client for {self.name}: {e}")

    def execute_tool(self, tool_name: str, tool_func, *args, **kwargs):
        """Executes an underlying tool function with RBAC permission validation and security logging."""
        if not permission_manager.check_permission(self.name, tool_name):
            raise PermissionError(f"Agent '{self.name}' is unauthorized to invoke tool '{tool_name}'")

        start_time = time.time()
        try:
            result = tool_func(*args, **kwargs)
            duration = time.time() - start_time
            log_agent_execution(self.name, tool_name, "SUCCESS", duration)
            return result
        except Exception as e:
            duration = time.time() - start_time
            log_agent_execution(self.name, tool_name, "FAILED", duration, details=str(e))
            raise e

    def process_request(self, user_prompt: str, context: dict = None) -> str:
        """
        Main entry point for processing user requests through security guardrails.
        """
        start_time = time.time()

        # 1. Rate Limiting Check
        allowed, msg = rate_limiter.is_allowed()
        if not allowed:
            return f"⚠️ {msg}"

        # 2. Input Length Check
        valid_text, msg = validator.validate_text_input(user_prompt)
        if not valid_text:
            return f"⚠️ {msg}"

        # 3. Prompt Injection Guardrail Check
        safe, reason = prompt_guard.is_safe(user_prompt)
        if not safe:
            log_agent_execution(self.name, "process_request", "REJECTED", time.time() - start_time, details=reason)
            return f"🚫 Request Rejected: {reason}"

        # 4. Save User Message to History
        memory_db.add_chat_message("user", self.name, user_prompt)

        # 5. Generate Response (Online Gemini API or Offline Fallback Engine)
        try:
            if self.client:
                response_text = self._call_gemini_api(user_prompt, context)
            else:
                response_text = self._generate_fallback(user_prompt, context)

            duration = time.time() - start_time
            log_agent_execution(self.name, "process_request", "SUCCESS", duration)

            # Save Assistant Response to History
            memory_db.add_chat_message("assistant", self.name, response_text)
            return response_text

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Error in agent {self.name}: {e}")
            log_agent_execution(self.name, "process_request", "ERROR", duration, details=str(e))
            
            # Fallback on API failure
            fallback = self._generate_fallback(user_prompt, context)
            memory_db.add_chat_message("assistant", self.name, fallback)
            return fallback

    def _call_gemini_api(self, prompt: str, context: dict = None) -> str:
        """Calls Google Gemini API using Google GenAI SDK."""
        system_instruction = f"You are {self.name}, an expert specialized study assistant agent. {self.description}"
        if context and context.get("document_text"):
            system_instruction += f"\n\nContext Document:\n{context['document_text'][:4000]}"

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"system_instruction": system_instruction}
        )
        return response.text

    @abstractmethod
    def _generate_fallback(self, prompt: str, context: dict = None) -> str:
        """Intelligent offline fallback generation engine when running without API key."""
        pass
