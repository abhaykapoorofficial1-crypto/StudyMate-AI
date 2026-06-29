from datetime import datetime
from agents.base_agent import BaseAgent
from mcp.calendar_server import calendar_mcp_server

class PlannerAgent(BaseAgent):
    """Specialized Agent for building personalized study timetables, revision plans, and countdown calendars."""

    def __init__(self):
        super().__init__(
            name="PlannerAgent",
            description="Specialist in study scheduling, exam countdowns, spaced repetition planning, and daily timetable optimization."
        )

    def _generate_fallback(self, prompt: str, context: dict = None) -> str:
        exam_date_str = "2026-08-15"
        exam_name = "Final Assessment"
        
        # Extract exam date if user provided YYYY-MM-DD in prompt
        import re
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", prompt)
        if date_match:
            exam_date_str = date_match.group(0)

        # Execute tool calls
        countdown = self.execute_tool("countdown_to_exam", calendar_mcp_server.countdown_to_exam, exam_date_str)
        schedule_data = self.execute_tool("create_study_schedule", calendar_mcp_server.create_study_schedule, exam_name, exam_date_str)

        response = f"### 📅 Personal Study & Revision Timetable\n"
        response += f"**Target Exam**: {exam_name} | **Exam Date**: `{exam_date_str}`\n"
        response += f"⏳ **Countdown**: `{countdown.get('days_remaining', 0)} Days Remaining` ({countdown.get('status', '')})\n\n"

        response += "#### 🗓️ Recommended Daily Schedule\n"
        response += "| Day | Date | Priority Topic | Focus Area | Daily Hours |\n"
        response += "|--- |--- |--- |--- |--- |\n"
        for slot in schedule_data["schedule"][:7]:
            response += f"| Day {slot['day']} | {slot['date']} | {slot['topic']} | {slot['task_type']} | {slot['allocated_hours']} hrs |\n"

        response += "\n💡 *Tip: Maintain consistency! Stick to 2-3 focused blocks of 45 minutes with short 10-minute breaks.*"
        return response

planner_agent = PlannerAgent()
