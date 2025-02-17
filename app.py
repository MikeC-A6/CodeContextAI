import streamlit as st
from src.ui.pages import MainPage

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Code Q&A Tool",
        page_icon="💻",
        layout="wide"
    )
    
    main_page = MainPage()
    main_page.render()

if __name__ == "__main__":
    main()
