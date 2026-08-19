import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not present.")

client=Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

def get_completions(messages, response_format):
    response=client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    return response.choices[0].message.content