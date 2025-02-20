"""
Manages UI state and loading messages for a consistent user experience.
Uses Streamlit's session state for persistence across reruns.
"""

import streamlit as st
from enum import Enum
from typing import Optional

class ProcessingState(Enum):
    """Enum for different processing states"""
    IDLE = "idle"
    EXTRACTING_REPO = "extracting_repo"
    ANALYZING_QUESTION = "analyzing_question"
    GENERATING_ANSWER = "generating_answer"
    ERROR = "error"

class UIStateManager:
    """Manages UI state and loading messages"""
    
    @staticmethod
    def init_session_state():
        """Initialize session state variables if they don't exist"""
        if 'processing_state' not in st.session_state:
            st.session_state.processing_state = ProcessingState.IDLE
        if 'error_message' not in st.session_state:
            st.session_state.error_message = None
        if 'code_context' not in st.session_state:
            st.session_state.code_context = None
        if 'status_complete' not in st.session_state:
            st.session_state.status_complete = False

    @staticmethod
    def set_state(state: ProcessingState, error_msg: Optional[str] = None):
        """Set the current processing state and optional error message"""
        st.session_state.processing_state = state
        st.session_state.error_message = error_msg
        st.session_state.status_complete = False

    @staticmethod
    def show_status():
        """Display appropriate status messages based on current state"""
        state = st.session_state.processing_state
        error_msg = st.session_state.error_message

        if state == ProcessingState.EXTRACTING_REPO:
            with st.status("Extracting code from repository...", expanded=True) as status:
                st.write("• Cloning repository")
                st.write("• Analyzing files")
                st.write("• Filtering relevant code")
                if not st.session_state.status_complete:
                    st.session_state.status_complete = True
                    st.rerun()
                status.update(label="Repository extracted!", state="complete", expanded=False)
        
        elif state == ProcessingState.ANALYZING_QUESTION:
            with st.status("Processing your question...", expanded=True) as status:
                st.write("• Identifying relevant files")
                st.write("• Analyzing code context")
                if not st.session_state.status_complete:
                    st.session_state.status_complete = True
                    st.rerun()
                status.update(label="Analysis complete!", state="complete", expanded=False)
                
        elif state == ProcessingState.GENERATING_ANSWER:
            with st.status("Generating answer...", expanded=True) as status:
                st.write("• Extracting code snippets")
                st.write("• Formulating detailed response")
                if not st.session_state.status_complete:
                    st.session_state.status_complete = True
                    st.rerun()
                status.update(label="Answer generated!", state="complete", expanded=False)
                
        elif state == ProcessingState.ERROR and error_msg:
            st.error(f"⚠️ {error_msg}")

    @staticmethod
    def clear_state():
        """Reset the state to idle"""
        st.session_state.processing_state = ProcessingState.IDLE
        st.session_state.error_message = None
        st.session_state.status_complete = False 