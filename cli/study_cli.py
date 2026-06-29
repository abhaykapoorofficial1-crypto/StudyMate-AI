import sys
import argparse
from pathlib import Path

# Add project root directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.explain_agent import explain_agent
from agents.quiz_agent import quiz_agent
from agents.notes_agent import notes_agent
from agents.planner_agent import planner_agent
from agents.flashcard_agent import flashcard_agent
from agents.progress_agent import progress_agent
from agents.memory_agent import memory_agent
from mcp.file_server import file_mcp_server
from mcp.pdf_server import pdf_mcp_server
from mcp.search_server import search_mcp_server

def main():
    parser = argparse.ArgumentParser(description="StudyMate AI - Secure Agentic CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # study-agent explain "Topic"
    explain_parser = subparsers.add_parser("explain", help="Explain a concept")
    explain_parser.add_argument("topic", type=str, help="Topic to explain")

    # study-agent summarize filename
    summarize_parser = subparsers.add_parser("summarize", help="Summarize a document")
    summarize_parser.add_argument("filename", type=str, help="Document filename")

    # study-agent notes filename/topic
    notes_parser = subparsers.add_parser("notes", help="Generate revision notes")
    notes_parser.add_argument("target", type=str, help="Target document filename or topic")

    # study-agent flashcards filename/topic
    flashcards_parser = subparsers.add_parser("flashcards", help="Generate flashcards")
    flashcards_parser.add_argument("target", type=str, help="Target document filename or topic")

    # study-agent quiz filename/topic
    quiz_parser = subparsers.add_parser("quiz", help="Generate a quiz")
    quiz_parser.add_argument("target", type=str, help="Target document filename or topic")

    # study-agent planner --exam-date YYYY-MM-DD
    planner_parser = subparsers.add_parser("planner", help="Generate study schedule")
    planner_parser.add_argument("--exam-date", type=str, default="2026-08-15", help="Exam date (YYYY-MM-DD)")

    # study-agent dashboard
    subparsers.add_parser("dashboard", help="Display progress dashboard metrics")

    # study-agent history
    subparsers.add_parser("history", help="View chat & document history")

    # study-agent upload filepath
    upload_parser = subparsers.add_parser("upload", help="Upload a study document")
    upload_parser.add_argument("filepath", type=str, help="Path to PDF, DOCX, or TXT file")

    # study-agent search "query"
    search_parser = subparsers.add_parser("search", help="Search notes & uploaded documents")
    search_parser.add_argument("query", type=str, help="Search query string")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    print("=" * 60)
    print(f"🤖 StudyMate AI Agent CLI | Command: {args.command.upper()}")
    print("=" * 60 + "\n")

    if args.command == "explain":
        res = explain_agent.process_request(args.topic)
        print(res)

    elif args.command == "summarize":
        content = pdf_mcp_server.read_pdf(args.filename) if Path(args.filename).exists() else ""
        ctx = {"document_text": content} if content else None
        res = notes_agent.process_request(f"summarize {args.filename}", context=ctx)
        print(res)

    elif args.command == "notes":
        content = pdf_mcp_server.read_pdf(args.target) if Path(args.target).exists() else ""
        ctx = {"document_text": content} if content else None
        res = notes_agent.process_request(args.target, context=ctx)
        print(res)

    elif args.command == "flashcards":
        res = flashcard_agent.process_request(args.target)
        print(res)

    elif args.command == "quiz":
        res = quiz_agent.process_request(args.target)
        print(res)

    elif args.command == "planner":
        res = planner_agent.process_request(f"planner --exam-date {args.exam_date}")
        print(res)

    elif args.command == "dashboard":
        res = progress_agent.process_request("dashboard metrics")
        print(res)

    elif args.command == "history":
        res = memory_agent.process_request("show history")
        print(res)

    elif args.command == "upload":
        p = Path(args.filepath)
        if not p.exists():
            print(f"❌ Error: File '{args.filepath}' not found.")
            return
        with open(p, "rb") as f:
            b = f.read()
        res = file_mcp_server.upload(p.name, b)
        if res.get("success"):
            print(f"✅ File uploaded successfully!\n- Filename: {res['filename']}\n- Type: {res['file_type']}\n- Size: {res['file_size']} bytes")
        else:
            print(f"❌ Upload failed: {res.get('error')}")

    elif args.command == "search":
        print(f"🔎 Searching for '{args.query}'...\n")
        notes_res = search_mcp_server.search_notes(args.query)
        docs_res = search_mcp_server.search_uploaded_documents(args.query)
        
        print("📌 Matching Notes:")
        for n in notes_res:
            print(f"- [{n['title']}] (Topic: {n['topic']})")
        if not notes_res:
            print("- No matching notes found.")

        print("\n📄 Matching Documents:")
        for d in docs_res:
            print(f"- [{d['filename']}] Snippet: {d['snippet']}")
        if not docs_res:
            print("- No matching documents found.")

if __name__ == "__main__":
    main()
