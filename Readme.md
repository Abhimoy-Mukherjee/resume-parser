# CVpulse

An AI-powered resume parser that extracts structured candidate data from a resume and scores how well it matches a given job description.

🔗 **Live demo:** https://cvpulse.onrender.com

*(Free-tier hosting — the app may take ~30-50 seconds to wake up if it's been idle.)*

## Status
Fully functional — full-stack web app, containerized and deployed.

## How it works
1. Upload a resume (`.pdf` or `.docx`) and paste a job description into the web UI.
2. On submit, the backend:
   - Parses the job description into structured fields (role, required/preferred skills, experience, education, responsibilities) via `analyze_job_description()`.
   - Extracts text from the resume and parses it into a structured schema (`Resume` model) via `parse_resume()`.
   - Scores the resume against the job description via `final_score()`, returning a match percentage, matching/missing skills, and improvement suggestions.
3. Results are displayed instantly in the browser, color-coded by match quality.

## Tech stack
- **Backend:** FastAPI, Python (uv for dependency/environment management)
- **AI:** Groq API (`openai/gpt-oss-120b`) for LLM-based parsing and scoring
- **Validation:** Pydantic schemas for structured, consistent LLM output
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Deployment:** Docker, Render
- **Reliability:** Rate-limited (5 requests/hour per IP) to protect the demo's API key from abuse

## Project structure
- `api.py` — FastAPI app; exposes `/analyze` endpoint, serves the frontend as static files
- `read.py` — extracts raw text from PDF/DOCX resumes
- `parse_resume.py` — parses resume text into structured data; scores resume against job description
- `job_description.py` — parses job description text into structured data
- `llm_client.py` — wraps Groq API calls
- `frontend/` — web UI (upload form, results display)
- `Dockerfile`, `docker-compose.yml` — containerization

## Running locally
```bash
uv sync
uv run uvicorn api:app --reload
```
Visit `http://127.0.0.1:8000`

Or with Docker:
```bash
docker compose up --build
```

## Setup
1. Clone the repo and install dependencies with `uv sync`.
2. Create a `.env` file with your Groq API key: