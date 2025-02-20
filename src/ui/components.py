import streamlit as st

class UIComponents:
    """Reusable UI components"""

    @staticmethod
    def show_input_selector() -> tuple[str, str | None]:
        """Display input method selector and return (method, input_data)"""
        input_method = st.radio(
            "Choose input method:",
            ["Upload JSONL file", "GitHub URL"],
            horizontal=True
        )
        
        if input_method == "Upload JSONL file":
            file_content = UIComponents.show_file_uploader()
            return ("file", file_content)
        else:
            github_url = UIComponents.show_github_input()
            return ("github", github_url)

    @staticmethod
    def show_file_uploader() -> str:
        """Display file upload widget"""
        uploaded_file = st.file_uploader("Upload JSONL file", type=["jsonl"])
        if uploaded_file:
            return uploaded_file.getvalue().decode("utf-8")
        return None

    @staticmethod
    def show_github_input() -> str:
        """Display GitHub URL input widget"""
        github_url = st.text_input(
            "Enter GitHub repository or subdirectory URL",
            placeholder="https://github.com/owner/repo/tree/branch/subdirectory"
        )
        if github_url:
            if not github_url.startswith("https://github.com/"):
                st.error("Please enter a valid GitHub URL starting with 'https://github.com/'")
                return None
            return github_url.strip()
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