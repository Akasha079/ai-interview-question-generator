# AI-Powered Interview Question Generator

An intelligent interview question generator that creates tailored, role-specific interview questions using AI (OpenAI) or built-in templates. Supports multiple job roles, question types, difficulty levels, and custom topics.

## Features

- **Multiple Job Roles**: Software Engineer, Data Scientist, Frontend Developer, DevOps Engineer, Product Manager
- **Question Types**: Technical, Behavioral, Situational, System Design, Coding
- **Difficulty Levels**: Easy, Medium, Hard, Expert
- **AI-Powered Generation**: Uses OpenAI GPT for dynamic question creation (optional)
- **Template Fallback**: Works without an API key using built-in question templates
- **Custom Topics**: Specify your own topics for targeted question generation
- **Export**: Download generated questions as JSON
- **Interviewer Notes**: Each question includes hints and sample answer points
- **REST API**: Fully accessible via API endpoints

## Tech Stack

- **Backend**: Python, Flask
- **AI**: OpenAI GPT-3.5/4
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Testing**: pytest

## Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key (optional — works without it using templates)

### Installation

```bash
# Clone and navigate
cd ai-interview-question-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key (optional)

# Run the application
python app.py
```

Open http://localhost:5000 in your browser.

## API Endpoints

### Generate Questions

```http
POST /api/generate
Content-Type: application/json

{
  "role": "software_engineer",
  "question_type": "technical",
  "difficulty": "medium",
  "num_questions": 5,
  "custom_topics": ["Docker", "Kubernetes"]
}
```

### Get Available Roles

```http
GET /api/roles
```

### Get Configuration

```http
GET /api/config
```

## Running Tests

```bash
pytest tests/ -v
```

## Project Structure

```
ai-interview-question-generator/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── api.py               # REST API endpoints
│   ├── generator.py         # Question generation engine
│   └── routes.py            # Web routes
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration & constants
├── static/
│   ├── css/style.css
│   └── js/app.js
├── templates/
│   └── index.html
├── tests/
│   └── test_generator.py
├── .env.example
├── .gitignore
├── app.py                   # Entry point
├── requirements.txt
└── README.md
```

## License

MIT
