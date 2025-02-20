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
       - github_url
    """

    def __init__(self, api_key: str, model_name: str):
        """
        :param api_key: Google Generative AI API key.
        :param model_name: The Gemini model identifier, e.g., 'models/gemini-2.0-flash'
        """
        try:
            # Configure the client with your API key.
            genai.configure(api_key=api_key)

            # Adjusted system instruction to emphasize thoroughness.
            self.model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=(
                    "You are a code analysis assistant acting as a retrieval-augmented generation (RAG) component. "
                    "Your job:\n"
                    "1. Analyze a user-provided question and a large codebase context.\n"
                    "2. Identify any files that are or might be relevant to the user's question. If there is any shred of doubt, "
                    "err on the side of inclusion.\n"
                    "3. For each relevant file, return a JSON object:\n"
                    "   {\n"
                    "     \"path\": \"...\",\n"
                    "     \"reason\": \"why it is or might be relevant\",\n"
                    "     \"github_url\": \"https://github.com/...\"\n"
                    "   }\n\n"
                    "Return only a JSON array of these objects and nothing else. If no files are relevant, return [].\n"
                    "Under no circumstances provide code snippets; only references. "
                    "When evaluating relevance, be broad but not indiscriminate: If a file is almost certainly irrelevant, do not include it. "
                    "However, if there's any potential link to the question, include it.\n"
                    "Exact JSON schema:\n"
                    "[\n"
                    "  {\n"
                    "    \"path\": \"...\",\n"
                    "    \"reason\": \"...\",\n"
                    "    \"github_url\": \"...\"\n"
                    "  }\n"
                    "]"
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
              "github_url": "https://github.com/..."
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
- "github_url": "https://github.com/.../blob/main/path/to/file"

If no files are relevant at all, return: []
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