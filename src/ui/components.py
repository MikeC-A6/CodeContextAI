import streamlit as st
from .state import UIStateManager, ProcessingState

class UIComponents:
    """Reusable UI components with improved UX"""

    @staticmethod
    def show_header():
        """Display the application header with description"""
        st.title("Code Q&A Tool")
        st.write(
            "Ask questions about any codebase by providing a GitHub URL or uploading a JSONL file. "
            "The tool will analyze the code and provide detailed answers using AI."
        )

    @staticmethod
    def show_input_selector() -> tuple[str, str | None]:
        """Display input method selector and return (method, input_data)"""
        # Initialize UI state
        UIStateManager.init_session_state()
        
        # Create two columns for the radio buttons, making GitHub URL the first option
        col1, col2 = st.columns([1, 1])
        with col1:
            github_selected = st.radio(
                "Choose input method:",
                ["GitHub URL", "Upload JSONL file"],
                label_visibility="collapsed",
                horizontal=True,
                key="input_method"
            ) == "GitHub URL"

        # Show the appropriate input field based on selection
        if github_selected:
            github_url = UIComponents.show_github_input()
            return ("github", github_url)
        else:
            file_content = UIComponents.show_file_uploader()
            return ("file", file_content)

    @staticmethod
    def show_file_uploader() -> str:
        """Display file upload widget with improved UX"""
        st.write("📄 Upload a JSONL file containing your code")
        uploaded_file = st.file_uploader(
            "Choose a JSONL file",
            type=["jsonl"],
            help="The file should be in JSONL format with each line containing a JSON object with 'path' and 'content' fields.",
            label_visibility="collapsed"
        )
        if uploaded_file:
            return uploaded_file.getvalue().decode("utf-8")
        return None

    @staticmethod
    def show_github_input() -> str:
        """Display GitHub URL input widget with improved UX"""
        st.write("🔗 Enter a GitHub repository or subdirectory URL")
        github_url = st.text_input(
            "GitHub URL",
            placeholder="https://github.com/owner/repo/tree/branch/subdirectory",
            help="You can enter a full repository URL or a specific subdirectory within a repository.",
            label_visibility="collapsed"
        )
        
        if github_url:
            if not github_url.startswith("https://github.com/"):
                st.error("Please enter a valid GitHub URL starting with 'https://github.com/'")
                return None
            return github_url.strip()
        return None

    @staticmethod
    def show_question_input() -> str:
        """Display question input widget with improved UX"""
        st.write("❓ Enter your question about the code")
        return st.text_area(
            "Your question",
            placeholder="Example: What does this code do? How is authentication handled?",
            help="Be as specific as possible to get the most accurate answer.",
            height=100,
            label_visibility="collapsed"
        )

    @staticmethod
    def show_results(snippets: str, answer: str):
        """Display results with improved formatting"""
        with st.expander("📚 Relevant Code Snippets", expanded=True):
            st.text_area(
                "",
                value=snippets,
                height=300,
                key="snippets_area",
                help="These are the most relevant code sections identified by Gemini."
            )

        st.subheader("🤖 AI Analysis")
        st.markdown(answer)

    @staticmethod
    def show_error(message: str):
        """Display error message with improved visibility"""
        st.error(f"⚠️ {message}")

    @staticmethod
    def show_processing_button(label: str = "Get Answer") -> bool:
        """Display a processing-aware button"""
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            return st.button(
                label,
                type="primary",
                use_container_width=True,
                disabled=st.session_state.processing_state != ProcessingState.IDLE
            )