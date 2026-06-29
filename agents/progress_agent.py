from agents.base_agent import BaseAgent
from memory.sqlite_memory import memory_db

class ProgressAgent(BaseAgent):
    """Specialized Agent for tracking learning metrics, analyzing performance, and recommending weak topic reviews."""

    def __init__(self):
        super().__init__(
            name="ProgressAgent",
            description="Specialist in performance analytics, study progress tracking, weak area identification, and gamification metrics."
        )

    def _generate_fallback(self, prompt: str, context: dict = None) -> str:
        metrics = memory_db.get_user_metrics()
        prog = metrics["progress"]
        gami = metrics["gamification"]

        response = "### 📊 Study Progress & Performance Analytics Report\n\n"
        response += f"🔥 **Current Study Streak**: `{gami['streak']} Days` | ⚡ **Total XP**: `{gami['xp']} Points`\n"
        response += f"⏱️ **Total Study Hours**: `{prog['study_hours']} hrs` | 📝 **Quizzes Taken**: `{prog['quizzes_completed']}`\n\n"

        response += "#### 🏆 Achievement Badges Unlocked\n"
        for b in gami["badges"]:
            response += f"- 🏅 **{b}**\n"
        response += "\n"

        response += "#### 📚 Topics Covered\n"
        for t in prog["topics_covered"]:
            response += f"- ✅ {t}\n"
        response += "\n"

        response += "#### ⚠️ Recommended Weak Areas for Priority Revision\n"
        for w in prog["weak_areas"]:
            response += f"- 🎯 **{w}** (Recommended revision: 45 mins spaced repetition quiz)\n"
        response += "\n"

        response += "🚀 *Keep up the great work! Consistent daily practice increases long-term memory retention by 40%.*"
        return response

progress_agent = ProgressAgent()
