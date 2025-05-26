import os
import json
import re
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from io import BytesIO

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def get_nutrition_info_from_file(file_bytes: bytes, description: str = "") -> dict:
    try:
        img = Image.open(BytesIO(file_bytes)).convert("RGB")

        prompt = f"""
        You are a health-focused food nutrition assistant. You will be given an image of Indian food and an optional description.
        Your task is to return nutritional insights in structured JSON format.

        Output only this format (no explanation):
        {{
          "calories": "...",
          "protein": "...",
          "fat": "...",
          "carbs": "...",
          "additional_info": "...",
          "summary": "...",
          "score": 0-100
        }}

        Description: {description}
        """

        parts = [img, prompt]
        response = model.generate_content(parts)
        text = response.text.strip()

        # Safely extract JSON from the output
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        return {"error": "Gemini response did not contain valid JSON."}

    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}


def get_nutrition_info_from_file(file_bytes: bytes, description: str = "") -> dict:
    try:
        img = Image.open(BytesIO(file_bytes)).convert("RGB")

        prompt = f"""
        Provide approximate nutritional information for the Indian food shown in this image.
        If description is available, use it to improve accuracy.

        Return JSON only in this format:
        {{
          "calories": "...",
          "protein": "...",
          "fat": "...",
          "carbs": "...",
          "additional_info": "..."
        }}

        Description: {description}
        """

        parts = [img, prompt]
        response = model.generate_content(parts)
        text = response.text.strip()

        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        return {"error": "Gemini response did not contain valid JSON."}
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}
