import streamlit as st
from .components import UIComponents
from ..services.file_handler import FileHandler
from ..services.llm_chain import LLMChain

class MainPage:
    """Main application page"""
    
    def __init__(self):
        self.components = UIComponents()
        self.file_handler = FileHandler()
        self.llm_chain = LLMChain()

    def render(self):
        """Render the main page"""
        st.title("Code Q&A Tool")
        st.write("Upload a JSONL file containing code and ask questions about it.")

        # File upload section
        file_content = self.components.show_file_uploader()
        
        if file_content:
            try:
                parsed_data = self.file_handler.parse_jsonl(file_content)
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
                self.components.show_error(f"Error parsing file: {str(e)}")
