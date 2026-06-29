import io
import fitz # PyMuPDF
import docx
from pathlib import Path
from security.logging import logger

class PDFMCPServer:
    """MCP Server for handling document text extractions, searches, and summaries."""

    @classmethod
    def read_pdf(cls, file_path: str) -> str:
        """Reads and returns all text from a PDF, DOCX, or TXT file path."""
        path = Path(file_path)
        if not path.exists():
            return f"Error: File '{file_path}' not found."

        ext = path.suffix.lower()
        try:
            if ext == ".pdf":
                doc = fitz.open(path)
                text = "\n".join([page.get_text() for page in doc])
                return text
            elif ext == ".docx":
                doc = docx.Document(path)
                text = "\n".join([p.text for p in doc.paragraphs if p.text])
                return text
            elif ext == ".txt":
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read()
            else:
                return f"Error: Unsupported format '{ext}'."
        except Exception as e:
            logger.error(f"Error reading document {file_path}: {e}")
            return f"Error reading file: {str(e)}"

    @classmethod
    def extract_text(cls, file_bytes: bytes, filename: str) -> str:
        """Extracts text from uploaded byte contents."""
        ext = Path(filename).suffix.lower()
        try:
            if ext == ".pdf":
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                text = "\n".join([page.get_text() for page in doc])
                return text
            elif ext == ".docx":
                doc = docx.Document(io.BytesIO(file_bytes))
                text = "\n".join([p.text for p in doc.paragraphs if p.text])
                return text
            elif ext == ".txt":
                return file_bytes.decode("utf-8", errors="ignore")
            else:
                return "Unsupported file extension."
        except Exception as e:
            logger.error(f"Error extracting bytes for {filename}: {e}")
            return f"Extraction failed: {str(e)}"

    @classmethod
    def search_document(cls, text_content: str, query: str) -> list[str]:
        """Searches document text for matching query paragraphs or sentences."""
        if not text_content or not query:
            return []
        
        paragraphs = [p.strip() for p in text_content.split("\n") if p.strip()]
        matches = [p for p in paragraphs if query.lower() in p.lower()]
        return matches[:10]

    @classmethod
    def summarize_document(cls, text_content: str, max_sentences: int = 5) -> str:
        """Generates an automatic concise summary from text content."""
        if not text_content:
            return "No content provided to summarize."

        paragraphs = [p.strip() for p in text_content.split("\n") if len(p.strip()) > 40]
        if not paragraphs:
            return text_content[:500] + "..."

        # Select representative paragraphs
        summary_paragraphs = paragraphs[:max_sentences]
        return "\n\n".join(summary_paragraphs)

pdf_mcp_server = PDFMCPServer()
