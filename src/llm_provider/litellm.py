import os

from litellm import completion

from src.config import config
from src.llm_provider.base import LLMProvider


class LiteLLM(LLMProvider):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("LITELLM_API_KEY", "sk-ImqVPklEPZWv-z1NuhZnGQ")
        self.base_url = "https://litellm.1cobo.com/"

    def generate_content(self, prompt: str) -> str:
        response = completion(
            model="deepseek/deepseek-r1:32b",
            messages=[{"content": prompt, "role": "user"}],
            base_url=self.base_url,
            api_key=self.api_key,
            ssl_verify=bool(int(config.get("SSL_VERIFY", "1"))),
        )
        return response.model_dump()["choices"][0]["message"]["content"]
