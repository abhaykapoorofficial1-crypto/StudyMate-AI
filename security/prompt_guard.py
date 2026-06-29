import re
from security.logging import logger

class PromptGuard:
    """Enterprise-level prompt injection and jailbreak detection system."""

    BLOCKED_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"reveal\s+(the\s+)?system\s+prompt",
        r"show\s+(hidden\s+)?prompts?",
        r"steal\s+api\s+key",
        r"disregard\s+prior\s+rules",
        r"you\s+are\s+now\s+dan",
        r"override\s+system\s+instructions",
        r"forget\s+everything\s+above",
        r"output\s+your\s+initial\s+instructions",
        r"print\s+your\s+prompt"
    ]

    @classmethod
    def is_safe(cls, prompt: str) -> tuple[bool, str]:
        """
        Validates prompt against malicious patterns.
        Returns (is_safe, reason).
        """
        if not prompt or not prompt.strip():
            return True, ""

        clean_prompt = prompt.lower().strip()

        for pattern in cls.BLOCKED_PATTERNS:
            if re.search(pattern, clean_prompt):
                reason = f"Security Violation: Potential prompt injection/jailbreak detected ('{pattern}')."
                logger.warning(f"PROMPT REJECTED: {reason} | Input: '{prompt[:100]}...'")
                return False, reason

        return True, ""

prompt_guard = PromptGuard()
