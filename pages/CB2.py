import streamlit as st
import ollama
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Stream assistant responses
def stream_ollama(prompt):
    for chunk in ollama.chat(
        model="qwen2.5-coder:7b", messages=[{"role": "user", "content": prompt}], stream=True
    ):
        yield chunk["message"]["content"]

# Generate code for the assistant to run
def get_response_stream(user_prompt):
    prompt = f'''You are a data analyst assistant, you are working with a DataFrame called df with the 
    following columns {df.columns.tolist()}.
    
    First decide whether the question can be answered with a plot or not.
    If it requires a plot, plot it in Streamlit using plotly express.
    If it is more direct, use pandas methods and st.write() to display the answer.
    Do not import anything. Do not write anything else, only reply with code blocks.
    All responses should be in code blocks.

    This is the question:
    {user_prompt}
    '''
    for chunk in ollama.chat(model="qwen2.5-coder:7b", messages=[{"role": "user", "content": prompt}], stream=True):
        yield chunk["message"]["content"]

# Execute and persist all previous code blocks
@st.cache_data
def execute_and_persist():
    for block in st.session_state["code_blocks"]:
        try:
            exec(block, globals())
        except Exception as e:
            st.error(f"Error executing saved block:\n{e}")

# Main app logic
if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df
    st.title("💬 Data Chatbot")

    # Init session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "code_blocks" not in st.session_state:
        st.session_state["code_blocks"] = []

    # Option to clear outputs
    if st.button("🧹 Clear All Outputs"):
        st.session_state["code_blocks"] = []
        st.rerun()

    # Display previous chat
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Re-run all previous code blocks
    execute_and_persist()

    # User input
    if user_input := st.chat_input("Start typing..."):

        st.session_state["messages"].append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        # Assistant response (streamed)
        with st.chat_message("assistant"):
            with st.expander("show code", expanded=False):
                response_container = st.empty()
                full_response = ""
                for chunk in get_response_stream(user_input):
                    full_response += chunk
                    response_container.markdown(full_response)

            # Extract and execute code block
            try:
                code = full_response[9:-3]  # Trim ```python ... ```
                st.session_state["code_blocks"].append(code)
                exec(code, globals())
            except Exception as e:
                st.error(f"Error executing new code:\n{e}")

            # Save assistant message
            st.session_state["messages"].append({"role": "assistant", "content": full_response})

else:
    st.warning("📁 Please upload a file to get started.")
