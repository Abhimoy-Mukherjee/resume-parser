from pydantic import BaseModel
from llm_client import get_completions

class JobD(BaseModel):
    role: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: float | None
    education_requirements: list[str]
    responsibilities: list[str]

jobd_schema = JobD.model_json_schema()

system_prompt = f"""
    You are an expert HR assistant.

    Your job is to analyze job descriptions and extract
    structured information from them.

    Return ONLY valid JSON matching this schema:

    {jobd_schema}
    IMPORTANT:
    Do NOT return the schema itself.
    Do NOT return fields like "properties", "title" or "type".
    Fill the schema with actual information extracted from the job description.

    If minimum experience is not mentioned, return null.
    If information for a list is missing, return an empty list.
    Do not invent the information.
"""

def analyze_job_description(job_description: str):

    user_prompt = f"Analyze the following job description: {job_description}"

    message_system={
        "role" : "system",
        "content" : system_prompt
    }
    message_user={
        "role" : "user",
        "content" : user_prompt
    }
    response_format={
        "type" : "json_object"
    }

    messages=[message_system, message_user]
    answer=get_completions(messages, response_format)
    raw_json=answer

    import json
    job_data=json.loads(raw_json)
    job = JobD(**job_data)
    return job

# print(job.minimum_experience)
# print(job.education_requirements)