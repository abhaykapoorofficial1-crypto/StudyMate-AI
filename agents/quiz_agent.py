import json
from agents.base_agent import BaseAgent
from mcp.database_server import database_mcp_server

class QuizAgent(BaseAgent):
    """Specialized Agent for generating MCQs, True/False, Fill in the blanks, and Short Answer quizzes."""

    def __init__(self):
        super().__init__(
            name="QuizAgent",
            description="Specialist in generating comprehensive quizzes, multiple-choice questions, and knowledge assessment tests."
        )

    def generate_quiz_json(self, topic: str, quiz_type: str = "MCQ", num_questions: int = 4) -> dict:
        """Generates a structured quiz dictionary and saves it to database memory."""
        questions = []
        if quiz_type.upper() in ["MCQ", "MULTIPLE CHOICE"]:
            questions = [
                {
                    "id": 1,
                    "question": f"What is the main objective or characteristic of {topic}?",
                    "options": [
                        f"Primary structural protocol for {topic}",
                        "Random execution without constraints",
                        "Deprecated legacy algorithm",
                        "External hardware configuration"
                    ],
                    "answer": f"Primary structural protocol for {topic}",
                    "explanation": f"The primary design of {topic} revolves around structured protocols."
                },
                {
                    "id": 2,
                    "question": f"Which of the following best describes time complexity or operational efficiency in {topic}?",
                    "options": [
                        "O(1) Constant or O(log N) Logarithmic in optimized structures",
                        "O(N^3) Cubic overhead always",
                        "Unbounded memory usage",
                        "Non-deterministic runtime"
                    ],
                    "answer": "O(1) Constant or O(log N) Logarithmic in optimized structures",
                    "explanation": "Optimized implementations aim for efficient logarithmic runtime."
                },
                {
                    "id": 3,
                    "question": f"In real-world applications, where is {topic} most frequently applied?",
                    "options": [
                        "Scalable software architectures & database systems",
                        "Manual mechanical clocks",
                        "Analog signal modulation only",
                        "Unformatted raw storage"
                    ],
                    "answer": "Scalable software architectures & database systems",
                    "explanation": f"{topic} is essential in modern computing applications."
                },
                {
                    "id": 4,
                    "question": f"What key requirement must be satisfied when implementing {topic}?",
                    "options": [
                        "Proper boundary condition check & exception handling",
                        "Ignoring memory leaks",
                        "Bypassing data validation",
                        "Hardcoding secret credentials"
                    ],
                    "answer": "Proper boundary condition check & exception handling",
                    "explanation": "Robust software design requires proper boundary checking."
                }
            ]
        elif quiz_type.upper() in ["TRUE/FALSE", "TRUE FALSE"]:
            questions = [
                {
                    "id": 1,
                    "question": f"True or False: {topic} is widely utilized to optimize system modularity and efficiency.",
                    "options": ["True", "False"],
                    "answer": "True",
                    "explanation": f"Yes, {topic} is fundamental to modern efficient engineering."
                },
                {
                    "id": 2,
                    "question": f"True or False: {topic} requires infinite storage memory to execute operations.",
                    "options": ["True", "False"],
                    "answer": "False",
                    "explanation": f"No, {topic} operates within strict bounded resource constraints."
                }
            ]
        else: # Fill blanks / Short answer fallback
            questions = [
                {
                    "id": 1,
                    "question": f"Fill in the blank: The foundational core of __________ ({topic}) enables efficient data flow.",
                    "answer": topic,
                    "explanation": f"{topic} is the exact core concept."
                }
            ]

        quiz_id = self.execute_tool("save_quiz", database_mcp_server.save_quiz, topic, quiz_type, questions)
        return {"quiz_id": quiz_id, "topic": topic, "quiz_type": quiz_type, "questions": questions}

    def _generate_fallback(self, prompt: str, context: dict = None) -> str:
        topic = prompt.replace("quiz", "").replace("mcq", "").strip() or "General Knowledge"
        quiz_data = self.generate_quiz_json(topic, "MCQ")
        
        response = f"### 🧠 Quiz Generator: **{topic}**\n"
        response += f"*Quiz saved to memory (ID: {quiz_data['quiz_id']})*\n\n"
        
        for q in quiz_data["questions"]:
            response += f"**Q{q['id']}. {q['question']}**\n"
            for idx, opt in enumerate(q["options"]):
                letter = chr(65 + idx)
                response += f"- [{letter}] {opt}\n"
            response += f"*(Correct Answer: {q['answer']})*\n\n"

        return response

quiz_agent = QuizAgent()
