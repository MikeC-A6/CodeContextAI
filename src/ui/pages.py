import streamlit as st
from .components import UIComponents
from .state import UIStateManager, ProcessingState
from ..services.file_handler import FileHandler
from ..services.github_extractor import GitHubExtractor
from ..services.llm_chain import LLMChain

class MainPage:
    """Main application page with improved UX"""

    def __init__(self):
        self.components = UIComponents()
        self.file_handler = FileHandler()
        self.github_extractor = GitHubExtractor()
        self.llm_chain = LLMChain()

    def render(self):
        """Render the main page with improved UX and state management"""
        # Show header
        self.components.show_header()

        # Initialize state
        UIStateManager.init_session_state()

        # Show current status before any new operations
        UIStateManager.show_status()

        # Input section
        input_method, input_data = self.components.show_input_selector()

        try:
            # Process input if we have new data and we're not already processing
            if input_data and st.session_state.processing_state == ProcessingState.IDLE:
                # Set state to processing
                UIStateManager.set_state(ProcessingState.EXTRACTING_REPO)

                # Process the input
                try:
                    if input_method == "file":
                        parsed_data = self.file_handler.parse_jsonl(input_data)
                    else:  # github
                        parsed_data = self.github_extractor.extract_to_jsonl(input_data)

                    # Store processed code context
                    st.session_state.code_context = self.file_handler.extract_code_context(parsed_data)
                    UIStateManager.set_state(ProcessingState.IDLE)

                except Exception as e:
                    UIStateManager.set_state(ProcessingState.ERROR, str(e))
                    return

            # Show question input if we have code context
            if st.session_state.code_context:
                question = self.components.show_question_input()

                if question and self.components.show_processing_button():
                    try:
                        # Set analyzing state
                        UIStateManager.set_state(ProcessingState.ANALYZING_QUESTION)

                        # Get initial snippets
                        snippets, _ = self.llm_chain.process_query(
                            question, st.session_state.code_context
                        )
                        st.session_state.snippets = snippets

                        # Get final answer
                        UIStateManager.set_state(ProcessingState.GENERATING_ANSWER)
                        _, answer = self.llm_chain.process_query(
                            question, st.session_state.code_context
                        )

                        # Show results
                        self.components.show_results(st.session_state.snippets, answer)
                        UIStateManager.set_state(ProcessingState.IDLE)

                    except Exception as e:
                        UIStateManager.set_state(
                            ProcessingState.ERROR,
                            f"Error processing query: {str(e)}"
                        )

        except Exception as e:
            UIStateManager.set_state(
                ProcessingState.ERROR,
                f"Unexpected error: {str(e)}"
            )