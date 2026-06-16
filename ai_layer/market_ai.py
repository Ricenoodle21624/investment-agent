from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def run_ai(prompt: str):

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("[Gemini ERROR]", e)
        return None