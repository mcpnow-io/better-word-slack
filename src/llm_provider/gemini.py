from google import genai
from pydantic import BaseModel

from src.config import config
from src.llm_provider.base import LLMProvider


class Result(BaseModel):
    text: str


class Gemini(LLMProvider):
    def __init__(self):
        super().__init__()
        self.client = genai.Client(api_key=config["GEMINI_API_KEY"])

    def generate_content(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return response.text

    def generate_content_enhanced(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Result,
            },
        )

        return response.text
