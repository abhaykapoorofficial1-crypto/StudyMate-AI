from agents.base_agent import BaseAgent
from mcp.database_server import database_mcp_server

class NotesAgent(BaseAgent):
    """Specialized Agent for generating structured bullet notes, summaries, formula sheets, and mind maps."""

    def __init__(self):
        super().__init__(
            name="NotesAgent",
            description="Specialist in distillation of study content into executive summaries, bullet point revision sheets, and visual mind maps."
        )

    def generate_mind_map_mermaid(self, topic: str) -> str:
        """Generates a Mermaid.js flowchart string representing a mind map of the topic."""
        mermaid = f"""graph TD
    Root["{topic}"] --> Sub1["Core Principles"]
    Root --> Sub2["Key Architecture"]
    Root --> Sub3["Practical Applications"]
    
    Sub1 --> Leaf1["Definition & Scope"]
    Sub1 --> Leaf2["Foundational Axioms"]
    
    Sub2 --> Leaf3["Data Flow & Logic"]
    Sub2 --> Leaf4["Efficiency & Constraints"]
    
    Sub3 --> Leaf5["Industry Use-cases"]
    Sub3 --> Leaf6["Best Practices"]
"""
        return mermaid

    def _generate_fallback(self, prompt: str, context: dict = None) -> str:
        topic = prompt.strip() or "Study Subject"
        doc_text = context.get("document_text", "") if context else ""

        title = f"Structured Notes: {topic}"
        content = f"# 📝 Study Notes: {topic}\n\n"
        content += "## 🎯 Executive Summary\n"
        if doc_text:
            content += f"Summary distilled from document:\n> *{doc_text[:250].replace('\n', ' ')}...*\n\n"
        else:
            content += f"This revision guide outlines core principles, structural paradigms, and tactical review items for **{topic}**.\n\n"

        content += "## 📌 High-Yield Bullet Points\n"
        content += f"- **Definition**: {topic} refers to the systematic organization of principles to achieve operational accuracy.\n"
        content += "- **Primary Objective**: Reduce cognitive friction while maximizing performance throughput.\n"
        content += "- **Critical Rule**: Always validate inputs, handle edge cases, and maintain modular separation.\n"
        content += "- **Performance Metrics**: Measured via accuracy, time complexity, and scalability.\n\n"

        content += "## 📐 Formula Sheet / Key Expressions\n"
        content += "```math\n"
        content += f"Efficiency({topic}) = (Useful Work Output) / (Total Time Spent)\n"
        content += "Total Score = sum(Correct Answers) * Streak Multiplier\n"
        content += "```\n\n"

        content += "## 🧠 Mind Map Diagram\n"
        content += "```mermaid\n"
        content += self.generate_mind_map_mermaid(topic)
        content += "```\n"

        # Save note to DB memory using tool
        self.execute_tool("save_notes", database_mcp_server.save_notes, title, topic, content)

        return content

notes_agent = NotesAgent()
