from agents.base_agent import BaseAgent
from memory.sqlite_memory import memory_db
from mcp.database_server import database_mcp_server

class MemoryAgent(BaseAgent):
    """Specialized Agent for managing historical context, uploaded document indexing, and memory search."""

    def __init__(self):
        super().__init__(
            name="MemoryAgent",
            description="Specialist in session history retrieval, uploaded document context cross-referencing, and long-term memory maintenance."
        )

    def _generate_fallback(self, prompt: str, context: dict = None) -> str:
        history = self.execute_tool("load_history", database_mcp_server.load_history)
        chats = history["chats"]
        docs = history["documents"]

        response = "### 🧠 Memory & History Inspector\n\n"
        response += f"📁 **Indexed Uploaded Documents**: `{len(docs)} files`\n"
        for d in docs[:5]:
            response += f"- 📄 **{d['filename']}** ({d['file_type'].upper()}, {d['file_size']} bytes)\n"
        if not docs:
            response += "- *No documents uploaded yet.*\n"
        response += "\n"

        response += f"💬 **Recent Chat History Logs**: `{len(chats)} entries`\n"
        for c in chats[-5:]:
            role_icon = "👤" if c["role"] == "user" else "🤖"
            response += f"- {role_icon} **{c['agent']}** ({c['timestamp']}): {c['message'][:80]}...\n"

        return response

memory_agent = MemoryAgent()
