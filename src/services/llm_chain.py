from typing import Tuple
from ..models.base import LLMBase
from ..models.gemini import GeminiClient
from ..models.openrouter import OpenRouterClient

class LLMChain:
    """Orchestrates the two-step LLM chain"""
    
    def __init__(self):
        self.gemini = GeminiClient()
        self.o3_mini = OpenRouterClient()

    def process_query(self, question: str, code_context: str) -> Tuple[str, str]:
        """
        Process a query through the two-step chain
        Returns: Tuple of (Gemini's selection, o3-mini's answer)
        """
        # Step 1: Get relevant code snippets from Gemini
        relevant_snippets = self.gemini.generate(question, code_context)
        
        # Step 2: Get final answer from o3-mini
        final_answer = self.o3_mini.generate(question, relevant_snippets)
        
        return relevant_snippets, final_answer
