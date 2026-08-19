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
default_job_description="""
About Stripe
Stripe is a financial infrastructure platform for businesses. Millions of companies—from the world’s largest enterprises to the most ambitious startups—use Stripe to accept payments, grow their revenue, and accelerate new business opportunities. Our mission is to increase the GDP of the internet, and we have a staggering amount of work ahead. That means you have an unprecedented opportunity to put the global economy within everyone’s reach while doing the most important work of your career.

About the team
Our internship program will provide an opportunity to work on meaningful products that will grow the GDP of the internet. Through the internship, you will work with many systems and technologies, gain experience in systems design and testing, and have opportunities to present your work to your team and the wider org. Each intern has a dedicated intern manager, and every project is part of the team’s roadmap and will directly help Stripe’s mission.

What you’ll do
Every internship at Stripe centers around a real, legitimate project that our customers urgently need, touching many parts of our operations and stack. We will support you in shipping it. Yes, you will actually ship it. Some recent projects include rebuilding our statistics aggregation service, building new service discovery systems, and many user facing projects like making it easy to understand error messages on Stripe Checkout. As a Stripe intern, you'll be tackling important projects to increase global commerce, while working alongside exceptional people who insist on doing their best work. You’ll learn from people with high standards who are great at inspiring others to do more and go further. We value technical and personal growth, and see our internship program as a vehicle to foster both.

Responsibilities
Write software that will be used in production, and has meaningful impact to Stripe
Give and receive technical feedback through code reviews or design discussions
Collaborate with other engineers and cross-functional stakeholders to proactively seek and incorporate feedback
Learn quickly by asking great questions, by working with your intern manager and teammates effectively, and by communicating the status of your work clearly
Who you are
We’re looking for someone who meets the minimum requirements to be considered for the role. If you meet these requirements, you are encouraged to apply. The preferred qualifications are a bonus, not a requirement.

Minimum requirements
A strong fundamental understanding of computer science through pursuit of a Bachelor’s, Master’s, or PhD degree in computer science, math, or a related discipline
Some experience and familiarity with programming, either through side projects or classwork. We work mostly in Java, Ruby, JavaScript, Scala, and Go. We believe new programming languages can be learned if the fundamentals and general knowledge are present
Experience from previous internships or other multi-person projects, including open source contributions, that demonstrate evaluating and receiving feedback from mentors, peers, and stakeholders
Ability to learn unfamiliar systems and form an understanding of those systems, through independent research and working with a mentor and subject matter experts
Preferred qualifications
* At least 2 years of university education, or equivalent work experience
One or more areas of specialized knowledge balanced with general skills and knowledge, such as knowing more frontend technologies and, at a high level, how a service handles an HTTP request
Understanding and some experience writing high quality pull requests, with good test coverage, and working knowledge to complete projects with minimal defects
Familiarity with navigating and managing your work in new code bases, with multiple languages
Ability to write clearly to explain your work to stakeholders, team members, and other Stripes
In-office expectations
Office-assigned Stripes in most of our locations are currently expected to spend at least 50% of the time in a given month in their local office or with users. This expectation may vary depending on role, team and location. For example, Stripes in Stripe Delivery Center roles in Mexico City, Mexico, Bengaluru, India, and Dublin, Ireland work 100% from the office. Also, some teams have greater in-office attendance requirements, to appropriately support our users and workflows, which the hiring manager will discuss. This approach helps strike a balance between bringing people together for in-person collaboration and learning from each other, while supporting flexibility when possible.
"""

def analyze_job_description(job_description: str = default_job_description):

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