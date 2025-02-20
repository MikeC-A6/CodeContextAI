import streamlit as st
from .components import UIComponents
from ..services.file_handler import FileHandler
from ..services.github_extractor import GitHubExtractor
from ..services.llm_chain import LLMChain

class MainPage:
    """Main application page"""
    
    def __init__(self):
        self.components = UIComponents()
        self.file_handler = FileHandler()
        self.github_extractor = GitHubExtractor()
        self.llm_chain = LLMChain()

    def render(self):
        """Render the main page"""
        st.title("Code Q&A Tool")
        st.write("Upload a JSONL file or enter a GitHub URL to ask questions about the code.")

        # Input section
        input_method, input_data = self.components.show_input_selector()
        
        if input_data:
            try:
                # Process input based on method
                if input_method == "file":
                    parsed_data = self.file_handler.parse_jsonl(input_data)
                else:  # github
                    parsed_data = self.github_extractor.extract_to_jsonl(input_data)
                
                code_context = self.file_handler.extract_code_context(parsed_data)
                
                # Question input section
                question = self.components.show_question_input()
                
                if st.button("Get Answer") and question:
                    with st.spinner("Processing your question..."):
                        try:
                            snippets, answer = self.llm_chain.process_query(
                                question, code_context
                            )
                            self.components.show_results(snippets, answer)
                        except Exception as e:
                            self.components.show_error(f"Error processing query: {str(e)}")
                            
            except ValueError as e:
                self.components.show_error(f"Error parsing input: {str(e)}")
            except Exception as e:
                self.components.show_error(f"Error: {str(e)}")
