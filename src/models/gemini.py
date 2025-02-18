import google.generativeai as genai

class LLMException(Exception):
    """Custom exception for errors in LLM usage."""
    pass

class GeminiClient:
    """
    A simplified Gemini client that:
    1. Accepts a question and a code context (read directly from a JSONL file).
    2. Passes a robust prompt to Gemini with all the code.
    3. Returns entire code files deemed relevant, erring on the side of including extra context.
    """

    def __init__(self, api_key: str, model_name: str):
        """
        :param api_key: The Google Generative AI API key.
        :param model_name: The Gemini model identifier
        """
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
        except Exception as e:
            raise LLMException(f"Failed to initialize Gemini: {str(e)}")

    def generate(self, question: str, code_context: str) -> str:
        """
        Call Gemini with a large code context and a user question.

        :param question: The user question or prompt.
        :param code_context: A large string containing code and metadata.
        :return: A text block containing the entire code files considered relevant.
        """
        try:
            prompt = f"""
            You are given a large codebase context below, and a question.
            Your task is to scan the code for any files that might help answer the question.
            For any file that seems relevant, return the entire code file with all its context.
            Do not summarize or condense the code.
            If you return a file and you think that there are other relevant files that help to complete the picture, return those files as well.
            Err on the side of including more code files if you think the content might be even slightly related to the question.
            Do not provide a complete solution to the question; your job is solely to identify and return
            the relevant code files in full.

            QUESTION:
            {question}

            CODEBASE CONTEXT (potentially large):
            {code_context}

            Please return your response as a list of entire code files, for example:

            RELEVANT CODE FILES:
            File: <file path>
            <full file content>

            File: <file path>
            <full file content>

            If no relevant files are found, respond with an empty or minimal output.
            """

            # Use generate_content() instead of generate()
            response = self.model.generate_content(
                contents=prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )

            # Check if the response was blocked
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                raise LLMException(f"Content blocked: {response.prompt_feedback.block_reason}")

            # Get the text from the response
            return response.text.strip()

        except Exception as e:
            if "429" in str(e):
                raise LLMException(
                    "API quota exceeded or rate limit. Try again later or reduce input size."
                )
            raise LLMException(f"Gemini generation failed: {str(e)}")