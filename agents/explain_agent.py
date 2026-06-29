from agents.base_agent import BaseAgent

class ExplainAgent(BaseAgent):
    """Specialized Agent for explaining concepts, breaking down complex topics, and providing step-by-step examples."""

    def __init__(self):
        super().__init__(
            name="ExplainAgent",
            description="Specialist in conceptual explanations, real-world analogies, step-by-step breakdowns, and simplified learning."
        )

    def _generate_fallback(self, prompt: str, context: dict = None) -> str:
        topic = prompt.strip()
        doc_text = context.get("document_text", "") if context else ""

        response = f"### 📚 Concept Explanation: **{topic}**\n\n"
        response += f"**Overview**:\n{topic} is a fundamental concept in study and computer science literature. "
        response += "It provides structured methodologies to solve complex analytical problems effectively.\n\n"
        
        response += "#### 💡 Real-World Analogy\n"
        response += f"Imagine organized books in a library or steps in a cooking recipe. Just like following instructions in sequence ensures a perfect meal, **{topic}** ensures systematic processing.\n\n"
        
        response += "#### 🔑 Core Pillars & Key Components\n"
        response += "1. **Input & Structure**: Organization of elements for seamless flow.\n"
        response += "2. **Processing Logic**: Core algorithms or principles executing operational rules.\n"
        response += "3. **Optimization & Efficiency**: Minimizing complexity and resource overhead.\n\n"

        if doc_text:
            response += "#### 📄 Document Insight\n"
            response += f"According to your uploaded document, key reference details include:\n> *\"{doc_text[:300].strip()}...\"*\n\n"

        response += "#### ⚡ Step-by-Step Example\n"
        response += "```python\n"
        response += f"# Demonstration of {topic} principle\n"
        response += "def demonstrate_concept(data):\n"
        response += f"    print(f'Processing {{data}} using {topic} principles...')\n"
        response += "    return [x * 2 for x in data]\n\n"
        response += "result = demonstrate_concept([1, 2, 3, 4])\n"
        response += "print('Result:', result)\n"
        response += "```\n\n"
        response += "*Tip: Would you like me to generate a practice quiz or summary notes on this topic?*"
        
        return response

explain_agent = ExplainAgent()
