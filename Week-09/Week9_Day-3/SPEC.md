# AI Email Reply Assistant - Project Specification

## 1. Project Name
**AI Email Reply Assistant**

---

## 2. Problem Statement
Writing clear, tone-appropriate email replies can be time-consuming, mentally draining, and stressful—especially for students, job applicants, and busy professionals who need to respond quickly without sacrificing communication quality. Many existing tools are overly complex, bloated with enterprise features, or expensive. 

**AI Email Reply Assistant** provides a lightweight, focused, and intuitive tool that allows users to paste an incoming email, choose a desired tone, and receive a high-quality, context-aware reply in seconds.

---

## 3. Target Users
- **Students**: Replying politely to professors, academic advisors, group project peers, and university administrators.
- **Job Seekers**: Responding to recruiter inquiries, interview invitations, follow-ups, and offer discussions.
- **Professionals**: Drafting daily workplace communications, team updates, and meeting acknowledgments efficiently.
- **Freelancers**: Communicating clearly and setting expectations with clients and prospective leads.

---

## 4. MVP Scope
The Minimum Viable Product (MVP) focuses strictly on three core features:

1. **Email Input**: A clean text area where the user can paste or type the received email body.
2. **Tone Selection**: A dropdown or radio selection with three distinct tone choices:
   - `Professional`: Formal, polite, structured, and workplace-appropriate.
   - `Friendly`: Warm, conversational, welcoming, and approachable.
   - `Short and Concise`: Direct, brief, bullet-point friendly, and to the point without fluff.
3. **AI Reply Generation**: A one-click generation trigger that prompts Google Gemini AI to produce an email reply matching the selected tone and displays the generated reply clearly with a convenient copy-to-clipboard action.

---

## 5. Out of Scope (Explicitly Excluded for MVP)
To ensure rapid hackathon delivery and maintain a strict scope, the following features are intentionally **excluded**:
- ❌ User authentication, signup, and login (no JWT, OAuth, or sessions).
- ❌ Database storage (no PostgreSQL, SQLite, MongoDB, or message persistence).
- ❌ Direct Gmail / Outlook / IMAP / SMTP integration (no direct inbox reading or automatic sending).
- ❌ Complex frameworks like LangChain, LlamaIndex, or RAG / Vector databases.
- ❌ File attachments or document parsing (PDF, DOCX, etc.).
- ❌ Chat history / conversation threads.
- ❌ Payment gateways, subscriptions, or credit systems.
- ❌ Multi-language translation support (MVP focuses on English).

---

## 6. Tech Stack
- **Backend Framework**: Python 3.10+ / [FastAPI](https://fastapi.tiangolo.com/) (Async web framework for REST API)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/) (Running the FastAPI backend)
- **Frontend UI**: [Streamlit](https://streamlit.io/) (Interactive web interface)
- **AI Integration**: Google Gemini API via official SDK (`google-genai`)
- **Data Validation & Schemas**: [Pydantic v2](https://docs.pydantic.dev/)
- **HTTP Client**: `requests` (Used by Streamlit to invoke FastAPI backend)
- **Configuration & Environment Management**: `python-dotenv`

---

## 7. System Architecture

```
User (Browser)
      │
      ▼
Streamlit Frontend (Port: 8501)
      │
      │  HTTP POST /api/generate-reply (JSON payload)
      ▼
FastAPI Backend (Port: 8000)
      │
      │  google-genai SDK Prompt Request
      ▼
Google Gemini API (e.g., gemini-2.5-flash / gemini-1.5-flash)
      │
      │  Generated Text Response
      ▼
FastAPI Backend (Response Packaging)
      │
      │  HTTP 200 JSON Response
      ▼
Streamlit Frontend
      │
      ▼
User Views Generated Reply (Ready to Copy)
```

---

## 8. API Specification

### Endpoint: `POST /api/generate-reply`
Generates an email reply based on the incoming email content and selected tone.

#### Request Headers:
`Content-Type: application/json`

#### Request Body Schema (Pydantic Model):
```json
{
  "email_content": "Hi Alex, Could you send over the updated project report by 3 PM today? Thanks, Sarah",
  "tone": "Professional"
}
```

- `email_content` (`string`, required): The full text of the received email. Min length: 10 chars, Max length: 5000 chars.
- `tone` (`string`, required): One of `["Professional", "Friendly", "Short and Concise"]`.

#### Response Body Schema (Success - `200 OK`):
```json
{
  "reply": "Dear Sarah,\n\nThank you for reaching out. I have finalized the updated project report and attached it for your review ahead of the 3 PM deadline.\n\nPlease let me know if you need any additional adjustments.\n\nBest regards,\nAlex",
  "tone": "Professional"
}
```

#### Error Response Schema (`400 Bad Request` / `422 Unprocessable Entity` / `500 Internal Server Error`):
```json
{
  "detail": "Descriptive error message explaining what failed."
}
```

### Health Check Endpoint: `GET /health`
- **Response**: `{"status": "healthy"}`

---

## 9. Environment Variables

Create a `.env` file in the root folder with the following variables:

```env
# Google Gemini API Key
GEMINI_API_KEY="your-gemini-api-key-here"

# Gemini Model Selection (default: gemini-2.5-flash)
GEMINI_MODEL="gemini-2.5-flash"

# Backend API Configuration
BACKEND_HOST="127.0.0.1"
BACKEND_PORT=8000
BACKEND_API_URL="http://127.0.0.1:8000"
```

---

## 10. Validation Rules
- **Email Content Validation**:
  - Must not be empty or whitespace-only.
  - Minimum length: 10 characters.
  - Maximum length: 5000 characters (prevents token overflow and abuse).
- **Tone Validation**:
  - Must strictly match one of the three allowed values: `Professional`, `Friendly`, `Short and Concise`.
- **Environment Validation**:
  - Ensure `GEMINI_API_KEY` is present on backend startup; return explicit configuration error if missing.

---

## 11. Error Handling Strategy
- **Frontend (Streamlit)**:
  - Validates non-empty input before firing network request.
  - Displays clear, user-friendly warnings (`st.warning` / `st.error`) if input is invalid or backend is unreachable.
  - Displays spinner while waiting for response (`with st.spinner("Generating reply..."): ...`).
- **Backend (FastAPI)**:
  - Input validation handled automatically via Pydantic (`422 Unprocessable Entity`).
  - Catches Gemini API exceptions (rate limits, quota issues, network timeouts) and returns a clean `500` or `503` status with human-readable error details.
  - Comprehensive server-side logging for easy debugging during the hackathon.

---

## 12. Testing Strategy
- **Manual Verification**:
  1. Test each of the 3 tones with sample emails (e.g., meeting request, recruiter message, project feedback).
  2. Test edge cases: empty input, extremely short input (<10 chars), large input (>5000 chars).
  3. Test backend failure behavior: invalid API key, offline backend.
- **Automated Smoke Tests**:
  - `pytest` suite testing:
    - Pydantic schema validation.
    - `/health` endpoint status.
    - Mocked `/api/generate-reply` endpoint testing valid and invalid payloads without consuming API quota.

---

## 13. Deployment Plan (Hackathon Demo & Local Setup)

### Local Development Setup
1. **Clone repository & prepare environment**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Configure `.env`**:
   Add valid `GEMINI_API_KEY`.
3. **Run Backend (FastAPI)**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. **Run Frontend (Streamlit)**:
   ```bash
   streamlit run app.py
   ```

### Hackathon Cloud Demo Options (Optional)
- **Frontend**: Streamlit Community Cloud (connected to GitHub repository).
- **Backend**: Render / Railway / Hugging Face Spaces (configured with `GEMINI_API_KEY` secret).
