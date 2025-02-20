from typing import Tuple
import json

from ..models.base import LLMBase
from ..models.gemini import GeminiClient
from ..models.openrouter import OpenRouterClient
from ..config import Config

# Import our new fetch_code utility
from .fetch_code import fetch_code_from_github

class LLMChain:
    """Orchestrates the two-step LLM chain"""

    def __init__(self):
        self.gemini = GeminiClient(
            api_key=Config.GOOGLE_API_KEY,
            model_name=Config.GEMINI_MODEL
        )
        self.o3_mini = OpenRouterClient()

    def process_query(self, question: str, code_context: str) -> Tuple[str, str]:
        """
        1) Query Gemini to get relevant file references (JSON string).
        2) For GitHub URLs, fetch raw code from each file.
        3) Pass the enriched JSON to o3-mini for the final answer.

        The code_context can be either:
        - Raw code context from GitHub extractor
        - JSONL file content

        In both cases, Gemini will return file references with GitHub URLs when possible.
        
        Returns: (Gemini's output JSON, o3-mini's answer string)
        """
        # Step 1: Gemini returns structured references
        gemini_output = self.gemini.generate(question, code_context)
        # e.g. '[{"path": "api/src/auth_utils.py","reason":"...","github_url":"..."}]'

        try:
            # Step 2: Try to convert GitHub URLs and fetch code
            # This will work for GitHub URLs and gracefully handle non-GitHub references
            code_payload = fetch_code_from_github(gemini_output)
        except Exception:
            # If fetching fails (e.g., not GitHub URLs), use the original context
            code_payload = json.dumps([{
                "path": "input.code",
                "reason": "Direct code input",
                "content": code_context
            }])

        # Step 3: Get final answer from o3-mini, passing the enriched code
        final_answer = self.o3_mini.generate(question, code_payload)

        return gemini_output, final_answer