from typing import Optional
import google.generativeai as genai
from .base import LLMBase, LLMException
from ..config import Config

class GeminiClient(LLMBase):
    def __init__(self):
        try:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        except Exception as e:
            raise LLMException(f"Failed to initialize Gemini: {str(e)}")

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        try:
            content_prompt = f"""
            Given the following code context, identify the most relevant code snippets 
            that would help answer this question: {prompt}

            Code context:
            {context}

            Return only the relevant code snippets and a brief explanation of why each 
            snippet is relevant. Format your response as:

            RELEVANT SNIPPETS:
            [code snippet 1]
            WHY: [brief explanation]

            [code snippet 2]
            WHY: [brief explanation]

            Keep your response focused and concise.
            """

            response = self.model.generate_content(
                content_prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )

            if response.prompt_feedback.block_reason:
                raise LLMException(f"Content blocked: {response.prompt_feedback.block_reason}")

            return response.text

        except Exception as e:
            if "429" in str(e):
                raise LLMException(
                    "API quota exceeded. Please try again later or reduce the size of the input."
                )
            raise LLMException(f"Gemini generation failed: {str(e)}")