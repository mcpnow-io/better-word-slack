import json

from src.llm_provider.base import LLMProvider
from src.prompts import BETTER_WORD_PROMPT


class BetterWordManager(object):
    @classmethod
    def get_llm_instance(cls) -> LLMProvider:
        from src.llm_provider.gemini import Gemini

        return Gemini()

    @classmethod
    def get_better_word(cls, text: str) -> str:
        prompt = BETTER_WORD_PROMPT.replace("{original_text}", text)
        max_retrys = 3
        llm_instance = cls.get_llm_instance()

        for _ in range(max_retrys):
            response = llm_instance.generate_content_auto(prompt)
            try:
                response_json = json.loads(response)
                return response_json["text"]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"{e}: Invalid response format: {response}")
                continue

        raise ValueError("Failed to get a valid response after multiple attempts.")
