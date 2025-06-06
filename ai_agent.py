### File: ai_agent.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_data_from_text(text):
    prompt = f"""
    Extract the following fields from this report message:
    - Name
    - Date
    - Location
    - Quantity

    Input: "{text}"
    Respond in JSON format like:
    {"name": "", "date": "", "location": "", "quantity": ""}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content.strip()
        import json
        return json.loads(content)
    except Exception as e:
        print("OpenAI Error:", e)
        return None