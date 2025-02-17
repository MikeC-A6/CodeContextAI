from typing import Optional, List, Dict
import google.generativeai as genai

class LLMException(Exception):
    """Custom exception for errors in LLM usage."""
    pass

class GeminiClient:
    """
    A more comprehensive Gemini client that:
    1. Accepts a question and a list of JSONL code entries (each with path, content, etc.).
    2. Optionally chunks or merges the code context.
    3. Passes a robust prompt to Gemini 2.0 Flash Lite with all relevant code lines.
    4. Returns multi-snippet output for each relevant file or excerpt, with a reason why it's relevant.
    """

    def __init__(self, api_key: str, model_name: str):
        """
        :param api_key: The Google Generative AI (Vertex) API key.
        :param model_name: The Gemini model identifier, e.g., 'models/text-bison-001'
        """
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
        except Exception as e:
            raise LLMException(f"Failed to initialize Gemini: {str(e)}")

    def _chunk_texts(
        self, texts: List[str], max_chars: int = 2000
    ) -> List[str]:
        """
        Optional helper to chunk large code strings into smaller chunks if needed.
        If not needed, you could omit or disable this.
        """
        chunks = []
        for txt in texts:
            if len(txt) <= max_chars:
                chunks.append(txt)
            else:
                start = 0
                while start < len(txt):
                    end = min(start + max_chars, len(txt))
                    chunks.append(txt[start:end])
                    start = end
        return chunks

    def build_context(
        self,
        code_entries: List[Dict],
        max_combined_chars: int = 30000
    ) -> str:
        """
        Convert a list of code entries (from .jsonl) into one large context string.
        Each entry might look like:
            {
              "path": "analytics/tests/test_cli.py",
              "language": "python",
              "content": "...(full code)...",
              ...
            }
        We'll collect them into a 'context block' that enumerates each file's path,
        then the code.

        :param code_entries: List of code entry dicts from the JSONL.
        :param max_combined_chars: If desired, you can limit total text appended.
        :return: A single string containing labeled code snippets.
        """
        lines_accumulated = []
        total_chars = 0

        for entry in code_entries:
            file_path = entry.get("path", "UNKNOWN_PATH")
            file_lang = entry.get("language", "unknown")
            file_content = entry.get("content", "")

            snippet_header = (
                f"\n=== FILE: {file_path}\n"
                f"LANGUAGE: {file_lang}\n"
                "SNIPPET:\n"
            )
            snippet = snippet_header + file_content.strip() + "\n"

            # If adding this snippet exceeds limit, optionally stop or chunk.
            if total_chars + len(snippet) > max_combined_chars:
                # chunk or skip
                chunked = self._chunk_texts([snippet], max_chars=2000)
                for c in chunked:
                    if total_chars + len(c) < max_combined_chars:
                        lines_accumulated.append(c)
                        total_chars += len(c)
                    else:
                        # If we can't fit more, we just break out
                        break
            else:
                lines_accumulated.append(snippet)
                total_chars += len(snippet)

        # Merge everything
        merged_context = "\n".join(lines_accumulated)
        return merged_context

    def generate(self, question: str, code_context: str) -> str:
        """
        Main method to call Gemini 2.0 Flash Lite with a big context and a user question.
        We request multi-snippet output, each snippet + reason.

        :param question: The user question or prompt.
        :param code_context: A large string containing code from .jsonl.
        :return: A text block enumerating relevant code snippets & reasons, e.g.:

        RELEVANT SNIPPETS:
        [code snippet 1]
        WHY: [brief explanation]

        [code snippet 2]
        WHY: [brief explanation]
        """
        try:
            prompt = f"""
            You are given a large codebase context below, and a question.
            Your task is to scan the code for any relevant files or code excerpts that
            might help answer the question. Then present those snippets along with
            a short reason why each is relevant. Do NOT provide a full solution answer
            to the question—just gather the relevant code.

            QUESTION:
            {question}

            CODEBASE CONTEXT (potentially large):
            {code_context}

            Please return your response in a multi-snippet format, like:

            RELEVANT SNIPPETS:
            [code snippet 1]
            WHY: [short explanation]

            [code snippet 2]
            WHY: [short explanation]

            If you do not find relevant code, respond with an empty or minimal snippet.
            """

            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )

            # Check if blocked or truncated
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                raise LLMException(f"Content blocked: {response.prompt_feedback.block_reason}")

            return response.text.strip()

        except Exception as e:
            if "429" in str(e):
                raise LLMException(
                    "API quota exceeded or rate limit. Try again later or reduce input size."
                )
            raise LLMException(f"Gemini generation failed: {str(e)}")
