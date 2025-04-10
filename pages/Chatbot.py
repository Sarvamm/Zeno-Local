import streamlit as st
import ollama
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def stream_ollama(prompt):
    for chunk in ollama.chat(model="qwen2.5-coder:7b", messages=[{"role": "user", "content": prompt}], stream=True):
        yield chunk["message"]["content"]

@st.cache_data
def execute(full_response):
    try:
        exec(full_response[9:len(full_response)-3], globals())
        
    except NameError as e:
        exec(full_response)
    except SyntaxError as e:
        exec(full_response)
        
    except Exception as e:
        st.error(f"Error executing code: {e}")
        response_container = st.empty()  # Placeholder for the streaming response
        full_response = ""
        for chunk in stream_ollama(f'''The following error was encountered while running:
                                {full_response}
                                    {e}
                                    Just tell in bullet points how to fix it.'''): 
            full_response += chunk
            response_container.markdown(full_response)
    finally: 
        st.session_state["messages"].append({"role": "assistant", "content": full_response})


def get_response_stream(user_prompt):
    prompt = f'''You are a data analyst assistant, you are working with a data called df with the 
     following columns {df.columns.tolist()} First decide whether the question can be answered with a plot or not.
     if the question requires a plot then plot it in streamlit using plotly express.
     If the question is more direct use pandas methods to answer the question and st.write() to display the answer.
     Under no circumstances should you use apostrophe or quotations.
     Do not import anything. Do no write anything else, only reply with code blocks. All responses should be in code blocks.

    This is the question:
    {user_prompt}
    '''
    for chunk in ollama.chat(model="qwen2.5-coder:7b", messages=[{"role": "user", "content": prompt}], stream=True):
        yield chunk["message"]["content"]

if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df
    st.title("💬 Chatbot")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

# Display chat history
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if user_input := st.chat_input("Start typing..."):

        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Stream the assistant's response
        with st.chat_message("Assistant"):
            with st.expander("show code", expanded=True):
                response_container = st.empty()  # Placeholder for the streaming response
                full_response = ""
                for chunk in get_response_stream(user_input):
                    full_response += chunk
                    response_container.markdown(full_response) 
            execute(full_response)
                
else:
    st.warning("Upload a file to get started.")





