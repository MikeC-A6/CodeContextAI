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
        """
        Generate a response using the o3-mini model via OpenRouter.

        The context can be:
          - Structured JSON from Gemini output (files + reasons + raw_url + code).
          - Additional string content.
        """
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
                                "3. Use **bold** text for important concepts\n"
                                "4. Maintain clear separation between code and explanations\n"
                                "5. Include a brief summary at the end\n\n"
                                "IMPORTANT:\n"
                                "- **Do not fabricate or infer code that is not provided in the 'code' field of the context.**\n"
                                "- Only include actual code snippets if they appear in the context's JSON.\n"
                                "- If you do quote code, ensure it's accurate and verbatim from the provided 'code' field."
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                f"You have been provided with structured JSON that may include code from "
                                f"one or more files. Each file object can have a 'code' field containing raw file content.\n\n"
                                f"CONTEXT:\n{context}\n\n"
                                f"**Task:** Provide a detailed, markdown-formatted answer to the following question:\n\n"
                                f"{prompt}\n\n"
                                "Structure your response with:\n"
                                "1. A clear introduction\n"
                                "2. Code analysis with properly formatted code blocks (only include code that is present in the 'code' field)\n"
                                "3. Detailed explanations under each section\n"
                                "4. A conclusion summarizing the key points"
                            )
                        }
                    ],
                    "temperature": 0.4,
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