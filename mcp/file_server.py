from pathlib import Path
from security.validators import validator
from security.logging import logger
from memory.sqlite_memory import memory_db
from mcp.pdf_server import pdf_mcp_server

class FileMCPServer:
    """MCP Server for managing uploaded document files."""

    @classmethod
    def upload(cls, filename: str, file_bytes: bytes) -> dict:
        """Validates, extracts text from, and saves uploaded file into SQLite database memory."""
        is_valid, reason = validator.validate_file(filename, file_bytes)
        if not is_valid:
            return {"success": False, "error": reason}

        text_content = pdf_mcp_server.extract_text(file_bytes, filename)
        ext = Path(filename).suffix.lower()
        file_size = len(file_bytes)

        memory_db.save_document(filename, ext, file_size, text_content)
        logger.info(f"FILE MCP: Uploaded '{filename}' ({file_size} bytes)")

        return {
            "success": True,
            "filename": filename,
            "file_type": ext,
            "file_size": file_size,
            "character_count": len(text_content)
        }

    @classmethod
    def delete(cls, filename: str) -> dict:
        """Deletes a document from storage."""
        memory_db.delete_document(filename)
        logger.info(f"FILE MCP: Deleted file '{filename}'")
        return {"success": True, "message": f"File '{filename}' successfully deleted."}

    @classmethod
    def list_files(cls) -> list[dict]:
        """Lists all uploaded document files with metadata."""
        return memory_db.get_all_documents()

file_mcp_server = FileMCPServer()
