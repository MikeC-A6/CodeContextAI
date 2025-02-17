import streamlit as st

class UIComponents:
    """Reusable UI components"""

    @staticmethod
    def show_file_uploader() -> str:
        """Display file upload widget"""
        uploaded_file = st.file_uploader("Upload JSONL file", type=["jsonl"])
        if uploaded_file:
            return uploaded_file.getvalue().decode("utf-8")
        return None

    @staticmethod
    def show_question_input() -> str:
        """Display question input widget"""
        return st.text_area("Enter your question about the code:", height=100)

    @staticmethod
    def show_results(snippets: str, answer: str):
        """Display results from the LLM chain"""
        st.subheader("Relevant Code Snippets (via Gemini)")
        st.text_area("", value=snippets, height=300, key="snippets_area")

        st.subheader("Final Answer (via o3-mini)")
        st.markdown(answer)

    @staticmethod
    def show_error(message: str):
        """Display error message"""
        st.error(message)