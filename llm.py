import google.genai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.environ["GOOGLE_GENAI_API_KEY"] 
MODEL = "gemini-2.0-flash"

client = genai.Client(api_key=API_KEY)

def generate_response(user_prompt: str, system_prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )
    return response.text