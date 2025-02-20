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
        2) Fetch raw code from each file using fetch_code_from_github().
        3) Pass that enriched JSON to o3-mini for the final answer.

        Returns: (Gemini's output JSON, o3-mini's answer string)
        """
        # Step 1: Gemini returns structured references
        gemini_output = self.gemini.generate(question, code_context)
        # e.g. '[{"path": "api/src/auth_utils.py","reason":"...","github_url":"..."}]'

        # Step 2: Convert to raw GitHub URLs and fetch actual code
        code_payload = fetch_code_from_github(gemini_output)
        # e.g. '[{"path": "...","reason":"...","github_url":"...","raw_url":"...","code":"<file contents>"}]'

        # Step 3: Get final answer from o3-mini, passing the enriched code
        final_answer = self.o3_mini.generate(question, code_payload)

        return gemini_output, final_answer