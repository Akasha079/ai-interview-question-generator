import os
from flask import Blueprint, request, jsonify
from app.generator import InterviewQuestionGenerator
from config.settings import Config, DifficultyLevel, QuestionType

api_bp = Blueprint("api", __name__)


def _get_generator():
    client = None
    if Config.OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
    return InterviewQuestionGenerator(openai_client=client)


@api_bp.route("/generate", methods=["POST"])
def generate_questions():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    role = data.get("role", "software_engineer")
    question_type = data.get("question_type", QuestionType.TECHNICAL)
    difficulty = data.get("difficulty", DifficultyLevel.MEDIUM)
    num_questions = min(int(data.get("num_questions", 5)), 15)
    custom_topics = data.get("custom_topics")

    if question_type not in QuestionType.ALL:
        return jsonify({"error": f"Invalid question type. Must be one of: {QuestionType.ALL}"}), 400
    if difficulty not in DifficultyLevel.ALL:
        return jsonify({"error": f"Invalid difficulty. Must be one of: {DifficultyLevel.ALL}"}), 400

    generator = _get_generator()

    try:
        questions = generator.generate_questions(
            role=role,
            question_type=question_type,
            difficulty=difficulty,
            num_questions=num_questions,
            custom_topics=custom_topics,
        )
        return jsonify({
            "success": True,
            "count": len(questions),
            "parameters": {
                "role": role,
                "question_type": question_type,
                "difficulty": difficulty,
            },
            "questions": questions,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/roles", methods=["GET"])
def get_roles():
    from config.settings import ROLE_TEMPLATES
    return jsonify({"roles": list(ROLE_TEMPLATES.keys())})


@api_bp.route("/config", methods=["GET"])
def get_config():
    return jsonify({
        "difficulties": DifficultyLevel.ALL,
        "question_types": QuestionType.ALL,
        "ai_enabled": bool(Config.OPENAI_API_KEY),
    })
