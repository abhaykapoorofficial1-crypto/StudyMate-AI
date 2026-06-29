# 📚 StudyMate AI – Secure Multi-Agent Study Assistant

<p align="center">
  <img src="assets/logo.png" alt="StudyMate AI Logo" width="180"/>
</p>

<p align="center">
  <strong>A production-ready AI-powered study assistant built with Google Agent Development Kit (ADK), Gemini, and Model Context Protocol (MCP).</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue" />
  <img src="https://img.shields.io/badge/Google-ADK-green" />
  <img src="https://img.shields.io/badge/Gemini-AI-orange" />
  <img src="https://img.shields.io/badge/MCP-Protocol-red" />
  <img src="https://img.shields.io/badge/Streamlit-Frontend-ff4b4b" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

---

# 🚀 Overview

StudyMate AI is a secure, intelligent, multi-agent learning platform that transforms static study materials into an interactive AI-powered learning experience.

Instead of relying on a single chatbot, StudyMate AI uses multiple specialized AI agents orchestrated with **Google ADK**. Each agent performs a dedicated task such as explaining concepts, generating quizzes, summarizing notes, planning study schedules, or tracking learning progress.

The system integrates **Model Context Protocol (MCP)** servers to securely access external tools like PDF processing, file management, databases, and scheduling while enforcing strict permissions and security policies.

---

# ✨ Features

## 📄 Smart Document Processing

* Upload PDF
* Upload DOCX
* Upload TXT
* AI-powered document understanding
* Semantic document search
* Intelligent document summarization

---

## 🤖 AI Learning Assistant

* Explain difficult concepts
* Generate summaries
* Create concise notes
* Build revision sheets
* Answer questions from uploaded documents

---

## 📝 Quiz Generator

Supports

* Multiple Choice Questions
* True/False
* Fill in the Blanks
* Short Answer Questions

---

## 📚 Flashcards

Generate AI-powered flashcards for faster revision.

---

## 📅 Study Planner

Create

* Daily plans
* Weekly schedules
* Revision plans
* Exam countdowns

---

## 📊 Progress Dashboard

Track

* Study hours
* Quiz scores
* Topics completed
* Weak concepts
* Learning streak
* Overall progress

---

## 💾 Persistent Memory

The assistant remembers

* Previous conversations
* Uploaded study materials
* Quiz history
* Study plans
* Weak topics
* Learning progress

---

# 🏗 Architecture

```
                  User
                    │
        Streamlit UI / Agent CLI
                    │
          Google ADK Router Agent
                    │
 ┌──────────┬──────────┬──────────┬──────────┐
 │          │          │          │          │
Explain   Quiz      Notes    Planner   Flashcards
 Agent    Agent      Agent     Agent      Agent
                    │
          Progress & Memory Agent
                    │
          Model Context Protocol
                    │
 ┌─────────┬─────────┬─────────┬─────────┐
 │         │         │         │
 PDF     Database   File     Calendar
 Server    Server    Server    Server
```

---

# 🧠 AI Agents

## Router Agent

Responsible for

* Intent detection
* Agent orchestration
* Workflow routing

---

## Explain Agent

* Explains concepts
* Provides examples
* Simplifies complex topics

---

## Quiz Agent

Creates

* MCQs
* True/False
* Fill in the blanks
* Short answers

---

## Notes Agent

Generates

* Smart summaries
* Revision notes
* Bullet notes
* Formula sheets

---

## Planner Agent

Creates

* Study schedules
* Revision plans
* Daily goals

---

## Flashcard Agent

Creates intelligent flashcards for active recall learning.

---

## Progress Agent

Tracks

* Learning progress
* Quiz performance
* Weak topics
* Recommendations

---

## Memory Agent

Stores

* Conversations
* Uploaded files
* User progress
* Personalized context

---

# 🔌 MCP Servers

## PDF Server

* Read PDF
* Extract text
* Search content
* Summarize chapters

---

## Database Server

* Save notes
* Save progress
* Load history
* Manage quizzes

---

## File Server

* Upload files
* Delete files
* List documents

---

## Calendar Server

* Study schedules
* Revision planner
* Exam countdown

---

## Search Server

* Search notes
* Search uploaded documents
* Semantic retrieval

---

# 🔒 Security Features

StudyMate AI follows secure AI engineering principles.

### Prompt Injection Protection

* Ignore previous instructions detection
* Jailbreak prevention
* Hidden prompt protection

### File Security

* MIME validation
* File size limits
* Safe upload handling

### Input Validation

* Prompt validation
* Filename validation
* Length restrictions

### Permission System

Each AI agent only accesses authorized MCP tools.

### Secret Management

* Environment variables
* No hardcoded API keys

### Logging

Logs include

* Timestamp
* Agent
* Tool
* Status
* Errors
* Execution time

### Rate Limiting

Protects against abuse and excessive requests.

---

# 💻 Agent CLI

Example commands

```bash
study-agent explain "Binary Tree"

study-agent summarize os.pdf

study-agent quiz dbms.pdf

study-agent notes python.pdf

study-agent planner --exam-date 2026-08-15

study-agent dashboard

study-agent history

study-agent upload networking.pdf
```

---

# 🖥 Streamlit Interface

Includes

* Chat Interface
* Document Upload
* Dashboard
* Flashcards
* Quiz
* Planner
* Notes
* Progress Analytics
* Dark Mode

---

# 📂 Project Structure

```
studymate-ai/

agents/
mcp/
security/
memory/
frontend/
cli/
config/
tests/
assets/

requirements.txt
README.md
.env.example
```

---

# ⚙ Installation

```bash
git clone https://github.com/yourusername/studymate-ai.git

cd studymate-ai

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY

DATABASE_URL=sqlite:///studymate.db

LOG_LEVEL=INFO
```

---

# ▶ Running the Project

Start Streamlit

```bash
streamlit run frontend/streamlit_app.py
```

Run Agent CLI

```bash
study-agent
```

Run ADK

```bash
adk web
```

---

# 🧪 Testing

```bash
pytest
```

---

# 📈 Future Improvements

* Voice conversations
* OCR support
* AI tutor avatars
* Multi-language support
* Mobile application
* Cloud deployment
* Team collaboration
* Real-time collaboration
* RAG optimization
* Vector database integration
* Offline mode

---

# 🛠 Tech Stack

* Python
* Google ADK
* Gemini API
* MCP
* Streamlit
* SQLite
* FastAPI
* PyMuPDF
* Pydantic
* Loguru
* Plotly
* Pandas

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Abhay Kapoor**

If you found this project helpful, consider giving it a ⭐ on GitHub!
