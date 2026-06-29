from memory.sqlite_memory import memory_db
from security.logging import logger

class SearchMCPServer:
    """MCP Server for cross-document and cross-note content search."""

    @classmethod
    def search_notes(cls, query: str) -> list[dict]:
        """Searches saved notes for relevant query matches."""
        if not query:
            return []
        
        notes = memory_db.get_all_notes()
        results = []
        q_lower = query.lower()

        for n in notes:
            if q_lower in n["title"].lower() or q_lower in n["topic"].lower() or q_lower in n["content"].lower():
                results.append(n)

        return results

    @classmethod
    def search_uploaded_documents(cls, query: str) -> list[dict]:
        """Searches extracted document texts for matching snippets."""
        if not query:
            return []

        docs = memory_db.get_all_documents()
        results = []
        q_lower = query.lower()

        for d in docs:
            full_text = memory_db.get_document_content(d["filename"])
            if q_lower in full_text.lower():
                # Extract snippet
                idx = full_text.lower().find(q_lower)
                start = max(0, idx - 100)
                end = min(len(full_text), idx + 200)
                snippet = "..." + full_text[start:end].replace("\n", " ") + "..."
                
                results.append({
                    "filename": d["filename"],
                    "file_type": d["file_type"],
                    "snippet": snippet
                })

        return results

search_mcp_server = SearchMCPServer()
