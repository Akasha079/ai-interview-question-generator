import pytest
from app.generator import InterviewQuestionGenerator
from config.settings import DifficultyLevel, QuestionType


@pytest.fixture
def generator():
    return InterviewQuestionGenerator()


def test_generate_technical_questions(generator):
    questions = generator.generate_questions(
        role="software_engineer",
        question_type=QuestionType.TECHNICAL,
        difficulty=DifficultyLevel.MEDIUM,
        num_questions=3,
    )
    assert len(questions) == 3
    for q in questions:
        assert "question" in q
        assert q["difficulty"] == DifficultyLevel.MEDIUM
        assert q["type"] == QuestionType.TECHNICAL


def test_generate_behavioral_questions(generator):
    questions = generator.generate_questions(
        role="product_manager",
        question_type=QuestionType.BEHAVIORAL,
        difficulty=DifficultyLevel.EASY,
        num_questions=2,
    )
    assert len(questions) == 2
    assert all(q["type"] == QuestionType.BEHAVIORAL for q in questions)


def test_custom_topics(generator):
    questions = generator.generate_questions(
        role="software_engineer",
        question_type=QuestionType.TECHNICAL,
        difficulty=DifficultyLevel.HARD,
        num_questions=2,
        custom_topics=["Kubernetes", "gRPC"],
    )
    assert len(questions) == 2


def test_all_question_types(generator):
    for qt in QuestionType.ALL:
        questions = generator.generate_questions(
            role="software_engineer",
            question_type=qt,
            difficulty=DifficultyLevel.MEDIUM,
            num_questions=1,
        )
        assert len(questions) == 1
        assert questions[0]["type"] == qt
