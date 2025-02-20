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
        
        # Input section
        input_method, input_data = self.components.show_input_selector()
        
        # Show current status if any
        status = UIStateManager.show_status()
        
        try:
            # Process input if we have new data
            if input_data:
                if st.session_state.processing_state == ProcessingState.IDLE:
                    try:
                        if input_method == "file":
                            parsed_data = self.file_handler.parse_jsonl(input_data)
                        else:  # github
                            UIStateManager.set_state(ProcessingState.EXTRACTING_REPO)
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
                
                if self.components.show_processing_button() and question:
                    try:
                        # Get initial snippets
                        UIStateManager.set_state(ProcessingState.ANALYZING_QUESTION)
                        st.rerun()
                        
                        snippets, _ = self.llm_chain.process_query(
                            question, st.session_state.code_context
                        )
                        
                        # Get final answer
                        UIStateManager.set_state(ProcessingState.GENERATING_ANSWER)
                        st.rerun()
                        
                        _, answer = self.llm_chain.process_query(
                            question, st.session_state.code_context
                        )
                        
                        # Show results
                        self.components.show_results(snippets, answer)
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
