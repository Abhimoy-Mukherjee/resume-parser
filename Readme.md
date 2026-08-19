# Resume Parser

A tool that parses resumes (PDF/DOCX), extracts structured candidate data using an LLM, and scores how well each candidate matches a given job description — ranking the top and bottom candidates automatically.

## Status
Functional — core features working

## How it works
1. Drop resumes (`.pdf` / `.docx`) into a `resumes/` folder.
2. Add your job description text to `job_description.txt`.
3. Run `main.py` — it will:
   - Parse the job description into structured fields (role, required/preferred skills, experience, education, responsibilities) via `analyze_job_description()`.
   - Extract text from each resume and parse it into a structured schema (`Resume` model) via `parse_resume()`.
   - Score each parsed resume against the job description via `final_score()`, returning a match percentage and details.
   - Print the top 2 and bottom 2 candidates by score.

## Tech stack
- Python (uv for dependency/environment management)
- Groq API (`openai/gpt-oss-120b`) for LLM-based parsing and scoring
- Pydantic for schema validation of parsed resume/job description/match result data

## Project structure
- `main.py` — orchestrates reading resumes, parsing, scoring, and ranking
- `read.py` — extracts raw text from PDF/DOCX resumes
- `parse_resume.py` — parses resume text into structured data; scores resume against job description
- `job_description.py` — parses job description text into structured data
- `llm_client.py` — wraps Groq API calls
- `job_description.txt` — plain text job description input (placeholder by default)

## Libraries
- pydantic
- python-dotenv
- groq
- pypdf
- python-docx

## Setup
1. Clone the repo and install dependencies with `uv sync` (or `uv add` per package if setting up fresh).
2. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_key_here
   ```
3. Replace the placeholder text in `job_description.txt` with an actual job description.
4. Add resumes to a `resumes/` folder (PDF or DOCX).
5. Run:
   ```
   uv run main.py
   ```

