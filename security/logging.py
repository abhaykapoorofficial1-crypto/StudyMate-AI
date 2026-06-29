import sys
from pathlib import Path
from loguru import logger
from config.settings import settings

# Configure Loguru logger
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logger.remove() # Remove default handler
logger.add(
    sys.stdout,
    level=settings.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:LOWERCASE}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
)
logger.add(
    log_dir / "audit.log",
    rotation="10 MB",
    retention="30 days",
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function} | {message}"
)

def log_agent_execution(agent_name: str, tool_name: str, status: str, duration_sec: float, details: str = ""):
    """Logs agent execution details for security and performance auditing."""
    logger.info(f"AGENT={agent_name} | TOOL={tool_name} | STATUS={status} | TIME={duration_sec:.3f}s | DETAILS={details}")
