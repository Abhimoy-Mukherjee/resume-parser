from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from read import read_pdf, read_docx
from parse_resume import parse_resume, final_score
from job_description import analyze_job_description
import tempfile
from pathlib import Path

app=FastAPI(title="Resume Parser API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.post("/analyze")
async def analyze_resume(resume_file: UploadFile=File(...), job_description:str=Form(...)):
    suffix=Path(resume_file.filename).suffix.lower()
    if suffix not in [".pdf",".docx"]:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
    with tempfile.NamedTemporaryFile(delete=False,suffix=suffix) as temp:
        contents=await resume_file.read()
        temp.write(contents)
        temp_path=Path(temp.name)
    try:
        if suffix==".pdf":
            resume_text=read_pdf(temp_path)
        else:
            resume_text=read_docx(temp_path)

        job=analyze_job_description(job_description)
        parsed_resume=parse_resume(resume_text)
        result=final_score(job,parsed_resume)
        return{
            "name":parsed_resume.name,
            "score":result.score,
            "details":result.details,
        }
    finally:
        temp_path.unlink(missing_ok=True)

@app.get("/")
def home():
    return {"message": "Resume Parser API is running"}

