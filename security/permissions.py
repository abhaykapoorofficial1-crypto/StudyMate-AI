from security.logging import logger

class PermissionManager:
    """Enforces agent-to-tool role-based access controls."""

    AGENT_PERMISSIONS = {
        "RouterAgent": ["*"], # Router can delegate to any tool/agent
        "ExplainAgent": ["read_pdf", "extract_text", "search_document", "search_notes", "load_history", "save_notes"],
        "QuizAgent": ["read_pdf", "extract_text", "save_quiz", "load_history", "save_progress"],
        "NotesAgent": ["read_pdf", "extract_text", "summarize_document", "save_notes", "search_notes"],
        "PlannerAgent": ["create_study_schedule", "revision_schedule", "countdown_to_exam", "load_history", "save_progress"],
        "FlashcardAgent": ["read_pdf", "extract_text", "save_notes", "load_history"],
        "ProgressAgent": ["save_progress", "load_history"],
        "MemoryAgent": ["load_history", "save_notes", "save_progress", "search_notes", "search_uploaded_documents"]
    }

    @classmethod
    def check_permission(cls, agent_name: str, tool_name: str) -> bool:
        allowed_tools = cls.AGENT_PERMISSIONS.get(agent_name, [])
        if "*" in allowed_tools or tool_name in allowed_tools:
            return True
        logger.warning(f"PERMISSION DENIED: Agent '{agent_name}' attempted to access restricted tool '{tool_name}'")
        return False

permission_manager = PermissionManager()
