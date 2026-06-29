import os
from pathlib import Path
from config.settings import settings
from security.logging import logger

class InputValidator:
    """Validates user text inputs and uploaded files."""

    MAX_PROMPT_LENGTH = 10000

    @classmethod
    def validate_text_input(cls, text: str) -> tuple[bool, str]:
        if not text or not text.strip():
            return False, "Input cannot be empty."
        if len(text) > cls.MAX_PROMPT_LENGTH:
            return False, f"Input exceeds maximum length of {cls.MAX_PROMPT_LENGTH} characters."
        return True, ""

    @classmethod
    def validate_file(cls, file_path: str | Path, file_bytes: bytes = None) -> tuple[bool, str]:
        path = Path(file_path)
        
        # Check extension
        ext = path.suffix.lower()
        if ext not in settings.allowed_extensions:
            return False, f"Invalid file type '{ext}'. Allowed types: {', '.join(settings.allowed_extensions)}"

        # Check file size
        if file_bytes is not None:
            size_mb = len(file_bytes) / (1024 * 1024)
        elif path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
        else:
            return False, "File does not exist."

        if size_mb > settings.max_file_size_mb:
            return False, f"File size ({size_mb:.2f}MB) exceeds limit of {settings.max_file_size_mb}MB."

        # Sanitize filename
        filename = path.name
        if ".." in filename or "/" in filename or "\\" in filename:
            return False, "Malicious path components detected in filename."

        return True, ""

validator = InputValidator()
