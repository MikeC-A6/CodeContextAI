from typing import Optional
import requests
from .base import LLMBase, LLMException
from ..config import Config

class OpenRouterClient(LLMBase):
    """Client for interacting with OpenRouter API to access the o3-mini model"""

    def __init__(self):
        self.base_url = Config.OPENROUTER_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Code Q&A Tool",
        }

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate a response using the o3-mini model via OpenRouter"""
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": Config.O3_MINI_MODEL,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a code analysis assistant that provides clear, well-structured "
                                "answers in markdown format. Your responses should:\n"
                                "1. Use markdown headers (##) to organize sections\n"
                                "2. Place code snippets in proper markdown code blocks with language tags\n"
                                "3. Use bold text (**) for important concepts\n"
                                "4. Maintain clear separation between code and explanations\n"
                                "5. Include a brief summary at the end"
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Based on these complete code files and any additional context that might help complete the picture:\n\n"
                                f"{context}\n\n"
                                f"Please provide a detailed, markdown-formatted answer to the following question:\n"
                                f"{prompt}\n\n"
                                "Structure your response with:\n"
                                "1. A clear introduction\n"
                                "2. Code analysis with properly formatted code blocks\n"
                                "3. Detailed explanations under each section\n"
                                "4. A brief conclusion summarizing the key points"
                            )
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 10000
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise LLMException(f"OpenRouter API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise LLMException(f"Failed to parse OpenRouter response: {str(e)}")
        except Exception as e:
            raise LLMException(f"OpenRouter generation failed: {str(e)}")
