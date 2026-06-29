import time
from collections import defaultdict
from config.settings import settings
from security.logging import logger

class RateLimiter:
    """Sliding window rate limiter."""

    def __init__(self):
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str = "default_user") -> tuple[bool, str]:
        now = time.time()
        window_start = now - 60.0 # 1 minute sliding window
        
        # Clean old timestamps
        self.requests[client_id] = [t for t in self.requests[client_id] if t > window_start]

        if len(self.requests[client_id]) >= settings.rate_limit_per_minute:
            logger.warning(f"RATE LIMIT EXCEEDED for client '{client_id}'")
            return False, "Rate limit exceeded. Please wait a moment before sending more requests."

        self.requests[client_id].append(now)
        return True, ""

rate_limiter = RateLimiter()
