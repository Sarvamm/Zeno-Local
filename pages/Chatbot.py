import streamlit as st
import ollama
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import traceback
import io
import contextlib

# --- Recorder class to persist st calls ---
class StreamlitCallRecorder:
    def __init__(self):
        self.calls = []

    def _record(self, method, *args, **kwargs):
        self.calls.append((method, args, kwargs))

    def write(self, *args, **kwargs): self._record("write", *args, **kwargs)
    def dataframe(self, *args, **kwargs): self._record("dataframe", *args, **kwargs)
    def table(self, *args, **kwargs): self._record("table", *args, **kwargs)
    def plotly_chart(self, *args, **kwargs): self._record("plotly_chart", *args, **kwargs)
    def markdown(self, *args, **kwargs): self._record("markdown", *args, **kwargs)
    def json(self, *args, **kwargs): self._record("json", *args, **kwargs)
    def line_chart(self, *args, **kwargs): self._record("line_chart", *args, **kwargs)
    def bar_chart(self, *args, **kwargs): self._record("bar_chart", *args, **kwargs)
    def area_chart(self, *args, **kwargs): self._record("area_chart", *args, **kwargs)

    def get_calls(self):
        return self.calls

# --- Ollama streaming ---
def stream_ollama(prompt):
    for chunk in ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    ):
        yield chunk["message"]["content"]

# --- Execute bot code ---
def execute(full_response):
    output_buffer = io.StringIO()
    recorder = StreamlitCallRecorder()
    error = None

    local_vars = {
        "df": st.session_state.df,
        "px": px,
        "sns": sns,
        "plt": plt,
        "pd": pd,
        "go": go,
        "st": recorder  # Redirect all st.* calls to the recorder
    }

    try:
        code = full_response.strip()[9:-3] if full_response.strip().startswith("```python") else full_response.strip()
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {}, local_vars)
    except Exception:
        error = traceback.format_exc()

    output_text = output_buffer.getvalue()
    return code, output_text, recorder.get_calls(), error

# --- Prompt builder ---
def get_response_stream(user_prompt):
    prompt = f'''You are a data analyst assistant, working with a DataFrame called df with the following columns:
{df.columns.tolist()}

First decide whether the question requires a plot or not.
- If yes, plot it using Plotly Express in Streamlit.
- If no, use pandas methods and display answers using st.write().

Use single quotes for st.write().
Respond only with executable Python code blocks that can run inside exec().

Question:
{user_prompt}
'''
    for chunk in ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    ):
        yield chunk["message"]["content"]

# --- Main App ---
if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df
    st.title("💬 Chatbot")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Show past messages
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(msg["content"])
            elif msg["role"] == "assistant":
                with st.expander("show code", expanded=False):
                    st.code(msg.get("code", ""), language="python")
                if msg.get("output"):
                    st.text("🧾 Output:")
                    st.code(msg["output"])
                if msg.get("st_calls"):
                    for method, args, kwargs in msg["st_calls"]:
                        if hasattr(st, method):
                            getattr(st, method)(*args, **kwargs)
                if msg.get("error"):
                    st.error(msg["error"])

    # Handle new user input
    if user_input := st.chat_input("Start typing..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""

            for chunk in get_response_stream(user_input):
                full_response += chunk
                with st.expander("show code", expanded=False):
                    response_container.markdown(full_response)

            # Execute the response as soon as it's fully streamed
            code, output, st_calls, error = execute(full_response)

            if output:
                st.text("🧾 Output:")
                st.markdown(output)
            if st_calls:
                for method, args, kwargs in st_calls:
                    if hasattr(st, method):
                        getattr(st, method)(*args, **kwargs)
            if error:
                st.error(error)

            st.session_state["messages"].append({
                "role": "assistant",
                "content": full_response,
                "code": code,
                "output": output,
                "st_calls": st_calls,
                "error": error
            })

else:
    st.warning("Upload a file to get started.")
