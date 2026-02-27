import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    MAX_QUESTIONS = int(os.getenv("MAX_QUESTIONS", "10"))
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))


class DifficultyLevel:
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

    ALL = [EASY, MEDIUM, HARD, EXPERT]


class QuestionType:
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SITUATIONAL = "situational"
    SYSTEM_DESIGN = "system_design"
    CODING = "coding"

    ALL = [TECHNICAL, BEHAVIORAL, SITUATIONAL, SYSTEM_DESIGN, CODING]


ROLE_TEMPLATES = {
    "software_engineer": {
        "topics": ["data structures", "algorithms", "system design", "OOP", "databases", "APIs"],
        "skills": ["Python", "Java", "JavaScript", "SQL", "Git", "Docker"],
    },
    "data_scientist": {
        "topics": ["machine learning", "statistics", "data wrangling", "deep learning", "NLP"],
        "skills": ["Python", "R", "SQL", "TensorFlow", "PyTorch", "Pandas"],
    },
    "frontend_developer": {
        "topics": ["HTML/CSS", "JavaScript", "React", "performance", "accessibility", "responsive design"],
        "skills": ["React", "TypeScript", "CSS", "Webpack", "Testing", "REST APIs"],
    },
    "devops_engineer": {
        "topics": ["CI/CD", "containerization", "cloud services", "monitoring", "infrastructure as code"],
        "skills": ["Docker", "Kubernetes", "AWS", "Terraform", "Jenkins", "Linux"],
    },
    "product_manager": {
        "topics": ["product strategy", "user research", "roadmapping", "metrics", "stakeholder management"],
        "skills": ["Agile", "Data Analysis", "Wireframing", "A/B Testing", "SQL"],
    },
}
