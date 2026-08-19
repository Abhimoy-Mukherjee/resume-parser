import os
from pathlib import Path
import time
from read import read_pdf, read_docx
from parse_resume import parse_resume, final_score
from job_description import analyze_job_description

jd_path=Path("job_description.txt")
job_description_text = jd_path.read_text(encoding="utf-8")
job = analyze_job_description(job_description_text)
resume_folder = Path("resumes")
all_results=[]
for file_path in resume_folder.iterdir():
    if file_path.suffix.lower() not in [".pdf", ".docx"]:
        continue
    print("\nProcessing:", file_path.name)
    if file_path.suffix.lower() == ".pdf":
        resume_text = read_pdf(file_path)
    elif file_path.suffix.lower() == ".docx":
        resume_text = read_docx(file_path)
    parsed_resume=parse_resume(resume_text)
    time.sleep(3)
    result = final_score(job, parsed_resume)
    time.sleep(3)
    print("Score:", result.score)
    all_results.append({
        "name": parsed_resume.name,
        "score": result.score,
        "details": result.details
    })
all_results.sort(
    key=lambda candidate: candidate["score"],
    reverse=True
)
top_2 = all_results[:2]
worst_2 = all_results[-2:]


print("TOP 2 CANDIDATES")
for candidate in top_2:

    print(
        candidate["name"],
        "-",
        candidate["score"],
        "%"
    )

    print(candidate["details"])

print("LOWEST 2 CANDIDATES")
for candidate in worst_2:

    print(
        candidate["name"],
        "-",
        candidate["score"],
        "%"
    )
    print(candidate["details"])