"""
GeminiClient (enhanced to err on the side of inclusion)

This module defines a GeminiClient that:
1. Accepts a question and a large codebase context.
2. Uses comprehensive system instructions to identify which files are relevant to the question.
3. Returns a JSON array of objects of the form:
   [
     {
       "path": "path/to/file",
       "reason": "why the file might be relevant",
       "github_url": "https://github.com/..."
     },
     ...
   ]
4. If no relevant files are found, returns [].

NOTES:
- This version heavily emphasizes including a file if there is any plausible reason it could be relevant.
- We keep the code-structure usage the same, but adjust the system prompt to encourage thoroughness.
"""

import google.generativeai as genai

class LLMException(Exception):
    """Custom exception for errors in LLM usage."""
    pass

class GeminiClient:
    """
    A Gemini client that:
    1. Takes a question and a codebase context (e.g. from a large JSONL or other source).
    2. Heavily emphasizes including any potentially relevant file references,
       even if you're not fully certain of its relevance.
    3. Returns a JSON array of file references, each containing:
       - path
       - reason
       - github_url (if from GitHub, otherwise a placeholder)
    """

    def __init__(self, api_key: str, model_name: str):
        """
        :param api_key: Google Generative AI API key.
        :param model_name: The Gemini model identifier, e.g., 'models/gemini-2.0-flash'
        """
        try:
            # Configure the client with your API key.
            genai.configure(api_key=api_key)

            # Adjusted system instruction to emphasize thoroughness and GitHub URL handling
            self.model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0,
                    top_p=1,
                    top_k=0,
                    max_output_tokens=50000,
                    response_mime_type="application/json"
                )
            )
        except Exception as e:
            raise LLMException(f"Failed to initialize Gemini: {str(e)}")

    def generate(self, question: str, code_context: str) -> str:
        """
        Calls the configured Gemini model with a codebase context and user question.
        Returns a JSON string with array of objects:
          [
            {
              "path": "api/src/something.py",
              "reason": "why it might be relevant",
              "github_url": "https://github.com/..." or "local://path/to/file"
            },
            ...
          ]
        or "[]" if no relevant files are found.
        """

        try:
            # Prompt includes the codebase context and the question
            prompt = f"""
QUESTION:
{question}

CODEBASE CONTEXT (potentially large):
{code_context}

Remember to err on the side of inclusion if there's any possibility of relevance.

Please return ONLY a valid JSON array of objects, each object with:
- "path": "file path"
- "reason": "why or how it may be relevant"
- "github_url": For GitHub files, use the full GitHub URL. For local files, use "local://" + file path

If no files are relevant at all, return: []

Example response for GitHub files:
[
  {{
    "path": "src/auth.py",
    "reason": "Contains authentication logic",
    "github_url": "https://github.com/org/repo/blob/main/src/auth.py"
  }}
]

Example response for local files:
[
  {{
    "path": "src/auth.py",
    "reason": "Contains authentication logic",
    "github_url": "local://src/auth.py"
  }}
]
"""

            # JSON schema that expects an array of objects
            schema = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string"
                        },
                        "reason": {
                            "type": "string"
                        },
                        "github_url": {
                            "type": "string"
                        }
                    },
                    "required": ["path", "reason", "github_url"]
                }
            }

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0,
                    top_p=1,
                    top_k=0,
                    max_output_tokens=50000,
                    response_mime_type="application/json",
                    response_schema=schema
                )
            )

            if response.prompt_feedback and response.prompt_feedback.block_reason:
                raise LLMException(f"Content blocked: {response.prompt_feedback.block_reason}")

            return response.text

        except Exception as e:
            if "429" in str(e):
                raise LLMException(
                    "API quota exceeded or rate limit. Try again later or reduce input size."
                )
            raise LLMException(f"Gemini generation failed: {str(e)}")