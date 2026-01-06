import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(user_prompt: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    result = json.loads(response.choices[0].message.content)
    return result