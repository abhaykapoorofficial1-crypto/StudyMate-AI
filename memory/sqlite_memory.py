import sqlite3
import json
from datetime import datetime
from pathlib import Path
from config.settings import settings
from security.logging import logger

class SQLiteMemory:
    """Persistent database memory manager using SQLite."""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.database_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT UNIQUE NOT NULL,
                    file_type TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Chats table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    agent TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Quizzes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quizzes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    quiz_type TEXT NOT NULL,
                    questions TEXT NOT NULL, -- JSON string
                    score REAL DEFAULT 0,
                    total_questions INTEGER DEFAULT 0,
                    completed INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Flashcards table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flashcards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    front TEXT NOT NULL,
                    back TEXT NOT NULL,
                    mastered INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Notes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Study Schedules table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS study_schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_name TEXT NOT NULL,
                    exam_date TEXT NOT NULL,
                    schedule_data TEXT NOT NULL, -- JSON string
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # User Progress table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    study_hours REAL DEFAULT 0.0,
                    quizzes_completed INTEGER DEFAULT 0,
                    topics_covered TEXT DEFAULT '[]', -- JSON array
                    weak_areas TEXT DEFAULT '[]', -- JSON array
                    last_active_date TEXT
                )
            """)

            # Gamification table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gamification (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    streak INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 100,
                    badges TEXT DEFAULT '["Quick Learner", "Study Mate Beginner"]', -- JSON array
                    last_streak_date TEXT
                )
            """)
            
            # Initialize default user progress & gamification row if empty
            cursor.execute("SELECT COUNT(*) FROM user_progress")
            if cursor.fetchone()[0] == 0:
                today = datetime.now().strftime("%Y-%m-%d")
                cursor.execute("INSERT INTO user_progress (study_hours, quizzes_completed, topics_covered, weak_areas, last_active_date) VALUES (2.5, 3, ?, ?, ?)",
                               (json.dumps(["Python Basics", "Data Structures", "Recursion"]), json.dumps(["Graph Algorithms"]), today))
            
            cursor.execute("SELECT COUNT(*) FROM gamification")
            if cursor.fetchone()[0] == 0:
                today = datetime.now().strftime("%Y-%m-%d")
                cursor.execute("INSERT INTO gamification (id, streak, xp, badges, last_streak_date) VALUES (1, 3, 250, ?, ?)",
                               (json.dumps(["Quick Learner", "Study Mate Beginner", "Quiz Master"]), today))

            conn.commit()
            logger.info("SQLite database initialized successfully.")

    # --- Document Methods ---
    def save_document(self, filename: str, file_type: str, file_size: int, content: str):
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO documents (filename, file_type, file_size, content) VALUES (?, ?, ?, ?)",
                (filename, file_type, file_size, content)
            )

    def get_all_documents(self):
        with self._get_connection() as conn:
            rows = conn.execute("SELECT filename, file_type, file_size, upload_date FROM documents ORDER BY upload_date DESC").fetchall()
            return [dict(r) for r in rows]

    def get_document_content(self, filename: str) -> str:
        with self._get_connection() as conn:
            row = conn.execute("SELECT content FROM documents WHERE filename = ?", (filename,)).fetchone()
            return row["content"] if row else ""

    def delete_document(self, filename: str):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM documents WHERE filename = ?", (filename,))

    # --- Chat History Methods ---
    def add_chat_message(self, role: str, agent: str, message: str):
        with self._get_connection() as conn:
            conn.execute("INSERT INTO chats (role, agent, message) VALUES (?, ?, ?)", (role, agent, message))

    def get_chat_history(self, limit: int = 50):
        with self._get_connection() as conn:
            rows = conn.execute("SELECT role, agent, message, timestamp FROM chats ORDER BY id ASC LIMIT ?", (limit,)).fetchall()
            return [dict(r) for r in rows]

    # --- Quiz Methods ---
    def save_quiz(self, topic: str, quiz_type: str, questions: list) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO quizzes (topic, quiz_type, questions, total_questions) VALUES (?, ?, ?, ?)",
                (topic, quiz_type, json.dumps(questions), len(questions))
            )
            return cursor.lastrowid

    def update_quiz_result(self, quiz_id: int, score: float):
        with self._get_connection() as conn:
            conn.execute("UPDATE quizzes SET score = ?, completed = 1 WHERE id = ?", (score, quiz_id))

    def get_quiz_history(self):
        with self._get_connection() as conn:
            rows = conn.execute("SELECT id, topic, quiz_type, score, total_questions, completed, created_at FROM quizzes ORDER BY created_at DESC").fetchall()
            return [dict(r) for r in rows]

    # --- Notes Methods ---
    def save_note(self, title: str, topic: str, content: str) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (title, topic, content) VALUES (?, ?, ?)", (title, topic, content))
            return cursor.lastrowid

    def get_all_notes(self):
        with self._get_connection() as conn:
            rows = conn.execute("SELECT id, title, topic, content, created_at FROM notes ORDER BY created_at DESC").fetchall()
            return [dict(r) for r in rows]

    # --- Flashcard Methods ---
    def save_flashcards(self, topic: str, cards: list[dict]):
        with self._get_connection() as conn:
            for card in cards:
                conn.execute(
                    "INSERT INTO flashcards (topic, front, back) VALUES (?, ?, ?)",
                    (topic, card.get("front", ""), card.get("back", ""))
                )

    def get_flashcards(self, topic: str = None):
        with self._get_connection() as conn:
            if topic:
                rows = conn.execute("SELECT id, topic, front, back, mastered FROM flashcards WHERE topic = ?", (topic,)).fetchall()
            else:
                rows = conn.execute("SELECT id, topic, front, back, mastered FROM flashcards ORDER BY created_at DESC").fetchall()
            return [dict(r) for r in rows]

    # --- Planner Methods ---
    def save_schedule(self, exam_name: str, exam_date: str, schedule: list) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO study_schedules (exam_name, exam_date, schedule_data) VALUES (?, ?, ?)",
                (exam_name, exam_date, json.dumps(schedule))
            )
            return cursor.lastrowid

    def get_latest_schedule(self):
        with self._get_connection() as conn:
            row = conn.execute("SELECT exam_name, exam_date, schedule_data FROM study_schedules ORDER BY id DESC LIMIT 1").fetchone()
            if row:
                d = dict(row)
                d["schedule_data"] = json.loads(d["schedule_data"])
                return d
            return None

    # --- Progress & Gamification Methods ---
    def get_user_metrics(self):
        with self._get_connection() as conn:
            prog = dict(conn.execute("SELECT * FROM user_progress LIMIT 1").fetchone())
            gami = dict(conn.execute("SELECT * FROM gamification WHERE id=1").fetchone())
            prog["topics_covered"] = json.loads(prog["topics_covered"])
            prog["weak_areas"] = json.loads(prog["weak_areas"])
            gami["badges"] = json.loads(gami["badges"])
            return {"progress": prog, "gamification": gami}

    def update_study_hours(self, added_hours: float):
        with self._get_connection() as conn:
            conn.execute("UPDATE user_progress SET study_hours = study_hours + ?", (added_hours,))

memory_db = SQLiteMemory()
