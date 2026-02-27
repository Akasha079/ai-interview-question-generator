from flask import Blueprint, render_template
from config.settings import DifficultyLevel, QuestionType, ROLE_TEMPLATES

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template(
        "index.html",
        roles=list(ROLE_TEMPLATES.keys()),
        difficulties=DifficultyLevel.ALL,
        question_types=QuestionType.ALL,
    )
