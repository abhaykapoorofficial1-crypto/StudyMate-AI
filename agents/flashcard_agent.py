from agents.base_agent import BaseAgent
from memory.sqlite_memory import memory_db

class FlashcardAgent(BaseAgent):
    """Specialized Agent for generating interactive Q&A flashcard decks."""

    def __init__(self):
        super().__init__(
            name="FlashcardAgent",
            description="Specialist in creating flashcard study decks for active recall and spaced repetition practice."
        )

    def generate_cards(self, topic: str, count: int = 5) -> list[dict]:
        cards = [
            {"front": f"What is the definition of {topic}?", "back": f"{topic} is a structured system framework engineered for optimal learning and execution."},
            {"front": f"What is a key advantage of using {topic}?", "back": "High efficiency, scalable execution, modular organization, and robust reliability."},
            {"front": f"What is a common pitfall when implementing {topic}?", "back": "Neglecting proper boundary conditions, skipping input validation, or poor memory allocation."},
            {"front": f"How does {topic} differ from basic monolithic approaches?", "back": f"{topic} enforces clear separation of concerns and component reusability."},
            {"front": f"What is the recommended best practice for reviewing {topic}?", "back": "Use spaced repetition across 1-day, 3-day, and 7-day intervals."}
        ]
        cards = cards[:count]
        memory_db.save_flashcards(topic, cards)
        return cards

    def _generate_fallback(self, prompt: str, context: dict = None) -> str:
        topic = prompt.replace("flashcards", "").replace("flashcard", "").strip() or "General Science"
        cards = self.generate_cards(topic)

        response = f"### 🎴 Flashcard Deck Generator: **{topic}**\n"
        response += f"*Generated and saved {len(cards)} flashcards to memory.*\n\n"

        for idx, c in enumerate(cards):
            response += f"**Card {idx+1}:**\n"
            response += f"- ❓ **Front**: {c['front']}\n"
            response += f"- 💡 **Back**: {c['back']}\n\n"

        response += "*Tip: You can study these interactively in the Streamlit Flashcards tab!*"
        return response

flashcard_agent = FlashcardAgent()
