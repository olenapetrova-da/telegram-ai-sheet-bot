import os
import openai
from dotenv import load_dotenv
import json

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_data_from_text(text):
    prompt = f"""
You are a data extraction assistant. Extract the following fields from the input message:

- name (a person's name)
- date (convert any format into DD.MM.YYYY)
- location (city or place, with the first letter capitalized)
- quantity (can be numeric or text with units)

The message may have unusual order, lowercase city names, or messy formatting — still try to extract and normalize the values.
Users may type fields in any order, use inconsistent casing, and write the date in formats like YYYY-MM-DD, DD/MM/YYYY, or 'June 3rd'.

Output JSON in this exact format:
{{
  "name": "Full Name",
  "date": "DD.MM.YYYY",
  "location": "City",
  "quantity": "value"
}}

Only return valid JSON — no explanation or formatting.

Input message: "{text}"
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()
        print("\n[DEBUG GPT Response]:", content)

        # remove markdown formatting if present (e.g., ```json ... ```)
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()

        return json.loads(content)

    except json.JSONDecodeError as json_err:
        print("⚠️ JSON parsing failed:", json_err)
        return None
    except Exception as e:
        print("OpenAI Error:", e)
        return None
