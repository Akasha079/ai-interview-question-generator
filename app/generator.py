import json
import random
from config.settings import ROLE_TEMPLATES, DifficultyLevel, QuestionType


class InterviewQuestionGenerator:
    """Generates interview questions using AI or template-based fallback."""

    DIFFICULTY_DESCRIPTORS = {
        DifficultyLevel.EASY: "basic, entry-level",
        DifficultyLevel.MEDIUM: "intermediate, requires practical experience",
        DifficultyLevel.HARD: "advanced, requires deep understanding",
        DifficultyLevel.EXPERT: "expert-level, requires extensive experience and mastery",
    }

    def __init__(self, openai_client=None):
        self.openai_client = openai_client

    def generate_questions(self, role, question_type, difficulty, num_questions=5, custom_topics=None):
        """Generate interview questions based on parameters."""
        if self.openai_client:
            return self._generate_with_ai(role, question_type, difficulty, num_questions, custom_topics)
        return self._generate_with_templates(role, question_type, difficulty, num_questions, custom_topics)

    def _build_prompt(self, role, question_type, difficulty, num_questions, custom_topics):
        """Build the prompt for AI-based generation."""
        topics_str = ", ".join(custom_topics) if custom_topics else "general topics"
        role_info = ROLE_TEMPLATES.get(role, {})
        if role_info and not custom_topics:
            topics_str = ", ".join(role_info.get("topics", []))

        difficulty_desc = self.DIFFICULTY_DESCRIPTORS.get(difficulty, "intermediate")
        role_display = role.replace("_", " ").title()

        return f"""Generate exactly {num_questions} {question_type} interview questions for a {role_display} position.

Difficulty level: {difficulty} ({difficulty_desc})
Topics to cover: {topics_str}

Requirements:
- Questions should be specific and actionable
- Include a mix of conceptual and practical questions
- Each question should test a different aspect of the candidate's knowledge
- For coding questions, describe the problem clearly
- For system design questions, provide context about scale

Return the response as a JSON array of objects with the following structure:
[
  {{
    "question": "The interview question text",
    "category": "The specific topic/category",
    "difficulty": "{difficulty}",
    "type": "{question_type}",
    "expected_skills": ["skill1", "skill2"],
    "hints": "Optional hint or what the interviewer should look for",
    "sample_answer_points": ["key point 1", "key point 2"]
  }}
]

Return ONLY the JSON array, no other text."""

    def _generate_with_ai(self, role, question_type, difficulty, num_questions, custom_topics):
        """Generate questions using OpenAI API."""
        prompt = self._build_prompt(role, question_type, difficulty, num_questions, custom_topics)

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical interviewer. Generate high-quality interview questions.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=3000,
        )

        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0]

        return json.loads(content)

    def _generate_with_templates(self, role, question_type, difficulty, num_questions, custom_topics):
        """Fallback template-based generation when no API key is available."""
        templates = self._get_templates(question_type)
        role_info = ROLE_TEMPLATES.get(role, {"topics": ["general"], "skills": ["general"]})
        topics = custom_topics or role_info.get("topics", ["general"])
        skills = role_info.get("skills", ["general"])

        questions = []
        used_templates = random.sample(templates, min(num_questions, len(templates)))

        for template in used_templates:
            topic = random.choice(topics)
            skill = random.choice(skills)
            question_text = template.format(topic=topic, skill=skill, role=role.replace("_", " "))

            questions.append({
                "question": question_text,
                "category": topic,
                "difficulty": difficulty,
                "type": question_type,
                "expected_skills": random.sample(skills, min(2, len(skills))),
                "hints": f"Look for understanding of {topic} concepts and practical experience.",
                "sample_answer_points": [
                    f"Demonstrates knowledge of {topic}",
                    f"Shows practical experience with {skill}",
                    "Communicates clearly and structured",
                ],
            })

        return questions

    def _get_templates(self, question_type):
        """Get question templates by type."""
        templates = {
            QuestionType.TECHNICAL: [
                "Explain the core concepts of {topic} and how you have applied them in your work.",
                "What are the trade-offs when choosing between different approaches to {topic}?",
                "How would you optimize a system that heavily relies on {topic}?",
                "Describe a challenging problem you solved using {skill}.",
                "What are common pitfalls when working with {topic}, and how do you avoid them?",
                "How do you stay current with best practices in {topic}?",
                "Explain the difference between various {topic} patterns and when to use each.",
                "Walk me through how you would debug a complex issue related to {topic}.",
                "What testing strategies do you use when working with {skill}?",
                "How would you design a {topic} solution that scales to millions of users?",
            ],
            QuestionType.BEHAVIORAL: [
                "Tell me about a time you had to learn {topic} quickly for a project deadline.",
                "Describe a situation where your approach to {topic} was challenged by a teammate.",
                "How do you handle disagreements about {topic} in a team setting?",
                "Tell me about a failure related to {topic} and what you learned from it.",
                "Describe how you mentored someone on {topic}.",
                "Tell me about a time you had to make a difficult decision regarding {topic}.",
                "How do you prioritize when working on multiple {topic}-related tasks?",
                "Describe a project where you led the {topic} implementation.",
            ],
            QuestionType.SITUATIONAL: [
                "If a production system related to {topic} went down, how would you handle it?",
                "How would you approach a project requiring {skill} with a very tight deadline?",
                "If you discovered a critical flaw in the {topic} architecture, what would you do?",
                "How would you onboard a new team member to a complex {topic} system?",
                "What would you do if the {topic} approach the team chose wasn't working?",
                "How would you handle a conflict between business requirements and {topic} best practices?",
            ],
            QuestionType.SYSTEM_DESIGN: [
                "Design a scalable system that incorporates {topic} for a large user base.",
                "How would you architect a microservices system centered around {topic}?",
                "Design a real-time {topic} processing pipeline.",
                "How would you design a fault-tolerant system using {skill}?",
                "Architect a {topic} system that handles 10,000 requests per second.",
                "Design a distributed {topic} system with eventual consistency.",
            ],
            QuestionType.CODING: [
                "Write a function that efficiently solves a common {topic} problem.",
                "Implement a data structure commonly used in {topic}.",
                "Write code to parse and process {topic}-related data efficiently.",
                "Implement an algorithm that optimizes {topic} performance.",
                "Write a solution for a real-world {topic} challenge using {skill}.",
                "Implement error handling and edge cases for a {topic} module.",
            ],
        }
        return templates.get(question_type, templates[QuestionType.TECHNICAL])
