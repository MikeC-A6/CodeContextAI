from typing import Optional
import requests
from .base import LLMBase, LLMException
from ..config import Config

class OpenRouterClient(LLMBase):
    def __init__(self):
        self.base_url = Config.OPENROUTER_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Code Q&A Tool",
        }

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": Config.O3_MINI_MODEL,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"""
                            Based on these relevant code snippets and explanations:
                            
                            {context}
                            
                            Please provide a clear and concise answer to this question:
                            {prompt}
                            """
                        }
                    ],
                    "temperature": 0.7
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            raise LLMException(f"OpenRouter generation failed: {str(e)}")
