from datetime import datetime, timedelta
from memory.sqlite_memory import memory_db
from security.logging import logger

class CalendarMCPServer:
    """MCP Server providing timetable and scheduling features."""

    @classmethod
    def countdown_to_exam(cls, target_date_str: str) -> dict:
        """Calculates exact days, hours, and status remaining until exam date (YYYY-MM-DD)."""
        try:
            target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
            now = datetime.now()
            delta = target_date - now
            
            days_left = max(0, delta.days)
            hours_left = max(0, int(delta.seconds / 3600))

            status = "Upcoming"
            if delta.days < 0:
                status = "Exam Completed"
            elif delta.days == 0:
                status = "EXAM TODAY!"
            elif delta.days <= 7:
                status = "CRITICAL REVISION PHASE"

            return {
                "exam_date": target_date_str,
                "days_remaining": days_left,
                "hours_remaining": hours_left,
                "status": status
            }
        except ValueError:
            return {"error": "Invalid date format. Please use YYYY-MM-DD."}

    @classmethod
    def create_study_schedule(cls, exam_name: str, exam_date_str: str, topics: list[str] = None) -> dict:
        """Generates a structured multi-day study schedule leading up to an exam."""
        countdown = cls.countdown_to_exam(exam_date_str)
        days_available = max(1, countdown.get("days_remaining", 7))

        if not topics:
            topics = ["Core Concepts", "Advanced Theories", "Problem Solving", "Mock Exams & Review"]

        schedule = []
        start_date = datetime.now()

        # Distribute topics across available days
        for i in range(min(days_available, 14)):
            date_curr = (start_date + timedelta(days=i)).strftime("%Y-%m-%d (%A)")
            topic = topics[i % len(topics)]
            task_type = "Theory & Practice" if i < days_available - 2 else "Final Revision & Mocks"
            schedule.append({
                "day": i + 1,
                "date": date_curr,
                "topic": topic,
                "task_type": task_type,
                "allocated_hours": 3.0
            })

        memory_db.save_schedule(exam_name, exam_date_str, schedule)
        return {
            "exam_name": exam_name,
            "exam_date": exam_date_str,
            "days_remaining": days_available,
            "schedule": schedule
        }

    @classmethod
    def revision_schedule(cls, weak_topics: list[str]) -> list[dict]:
        """Creates an intensive spaced repetition revision schedule for specified topics."""
        if not weak_topics:
            weak_topics = ["General Concepts Revision"]

        revision_plan = []
        intervals = [1, 3, 7, 14] # Spaced repetition days
        now = datetime.now()

        for idx, topic in enumerate(weak_topics):
            day_offset = intervals[idx % len(intervals)]
            rev_date = (now + timedelta(days=day_offset)).strftime("%Y-%m-%d")
            revision_plan.append({
                "topic": topic,
                "revision_date": rev_date,
                "session_focus": f"Spaced Repetition Review #{idx+1}",
                "recommended_minutes": 45
            })

        return revision_plan

calendar_mcp_server = CalendarMCPServer()
