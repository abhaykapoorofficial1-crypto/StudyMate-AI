from memory.sqlite_memory import memory_db
from security.logging import logger

class DatabaseMCPServer:
    """MCP Server providing database persistence functions."""

    @classmethod
    def save_progress(cls, study_hours: float = 0.0) -> dict:
        """Updates user study hours and returns updated metrics."""
        memory_db.update_study_hours(study_hours)
        return memory_db.get_user_metrics()

    @classmethod
    def save_notes(cls, title: str, topic: str, content: str) -> int:
        """Saves a study note into database memory."""
        note_id = memory_db.save_note(title, topic, content)
        logger.info(f"DB MCP: Saved note '{title}' (ID: {note_id})")
        return note_id

    @classmethod
    def save_quiz(cls, topic: str, quiz_type: str, questions: list) -> int:
        """Saves a generated quiz into database memory."""
        quiz_id = memory_db.save_quiz(topic, quiz_type, questions)
        logger.info(f"DB MCP: Saved quiz for topic '{topic}' (ID: {quiz_id})")
        return quiz_id

    @classmethod
    def load_history(cls, limit: int = 20) -> dict:
        """Loads conversation history, documents, and user progress."""
        chats = memory_db.get_chat_history(limit=limit)
        docs = memory_db.get_all_documents()
        metrics = memory_db.get_user_metrics()
        return {
            "chats": chats,
            "documents": docs,
            "metrics": metrics
        }

database_mcp_server = DatabaseMCPServer()
