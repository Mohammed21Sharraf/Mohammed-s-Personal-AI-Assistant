import streamlit as st
import requests
from streamlit.components.v1 import html
import os

st.set_page_config(
    page_title="Mohammed's Portfolio Assistant",
    page_icon="🤖",
    layout="centered"
)

def load_css():
    with open("styles/dark_theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("About Him")
    st.markdown("""
    Mohammed Sharraf, is passionate about Software Engineering, Machine Learning, 
    Deep Learning, and Natural Language Processing, 
    with a particular interest in NLP for Software Engineering, 
    such as Code Generation and Code Search. 
    He is also keen on exploring the applications of NLP,
    Multimodality in NLP, and Retrieval-Augmented Generation (RAG). 
    Currently, he is looking for a thesis-based master's opportunity
    to further his research and skills in these areas.
    He is naturally curious, love sharing knowledge,
    and enjoy engaging in insightful discussions. 
    Additionally, he has a strong passion for traveling and exploring new places. 
    """)
    st.markdown("""*Unfortunately, I hallucinate and cannot give the optimal answers for some of the queries.
                Mohammed is working on me for the fix. Thank you for understanding!*
                """)
    
st.title("Hi! I'm Mohammed's Portfolio Assistant 😄")
st.caption("Ask me about his experience, skills, or research work!")

if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        try:
            # Call your FastAPI backend
            response = requests.post(
                "http://localhost:8000/query",
                json={"question": prompt}
            )
            
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Error connecting to the AI server")
                
        except requests.exceptions.ConnectionError:
            st.error("Backend service unavailable. Please ensure the server is running.")