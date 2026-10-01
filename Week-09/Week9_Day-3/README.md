# AI Email Reply Assistant

A lightweight, intuitive tool designed to help students, job seekers, and professionals generate tone-appropriate email responses using Google Gemini AI.

## Project Structure (Cycle 1 - Foundation)

`	ext
ai-email-reply-assistant/
│
├── backend/
│   ├── __init__.py
│   └── main.py          # FastAPI application foundation
│
├── frontend/            # Streamlit UI (Coming in later cycles)
│
├── tests/
│   └── __init__.py      # Test suite directory
│
├── .gitignore           # Git ignore configuration
├── .env.example         # Template for environment variables
├── requirements.txt     # Python dependencies
├── SPEC.md              # Project specification & source of truth
└── README.md            # Project documentation
`

## Local Setup Instructions

1. **Clone the Repository & Navigate to Project**:
   `ash
   cd ai-email-reply-assistant
   `

2. **Create and Activate a Virtual Environment**:
   `ash
   # Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux:
   python3 -m venv venv
   source venv/bin/activate
   `

3. **Install Dependencies**:
   `ash
   pip install -r requirements.txt
   `

4. **Set Up Environment Variables**:
   `ash
   # Copy the example environment file
   # Windows:
   copy .env.example .env

   # macOS / Linux:
   cp .env.example .env
   `
   *Fill in your GEMINI_API_KEY in .env (required for upcoming AI cycles).*

## How to Run the FastAPI Backend

Run the FastAPI server using Uvicorn:

`ash
uvicorn backend.main:app --reload --port 8000
`

Once running, you can test the endpoints in your browser or with curl:
- Root endpoint: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- Interactive API Docs (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
