import streamlit as st
from streamlit_extras.buy_me_a_coffee import button
if "status" not in st.session_state:
    st.session_state.status = None
if 'questions' not in st.session_state:
    st.session_state.questions = None


#Page setup
HomePage = st.Page(
    page="pages/Overview.py",
    icon="🏠",
    title = "Data Overview",
    default = True
)
StatsPage = st.Page(
    page="pages/Statistics.py",
    icon="📊",
    title = "Data Profiling"
)
PlotsPage = st.Page(
    page="pages/Graph_Plots.py",
    icon="📈",
    title = "Plot Graphs"
)
ChatPage = st.Page(
    page="pages/Chatbot.py",
    icon="🤖",    
    title = "Chatbot"
)
AboutPage = st.Page(
    page="pages/About.py",
    icon="👤",    
    title = "About"
)


import requests
import subprocess
import time
status = st.sidebar.empty()
container  = st.sidebar.empty()

def is_ollama_running():
    try:
        response = requests.get("http://localhost:11434", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_ollama():
    try:
        with st.spinner("Starting Ollama..."):
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(3)
        st.session_state.status = "Online"  
    except Exception as e:
            status.error("Failed to start Ollama:" + str(e))

def list_installed_models():
    try:
        output = subprocess.check_output(["ollama", "list"], universal_newlines=True)
        models = [line.split()[0] for line in output.strip().split("\n")[1:]]
        return models
    except subprocess.CalledProcessError as e:
            container.error(f"Error listing models: {e}")
            return []

# --- Main logic ---
if st.session_state.status is None:
    if not is_ollama_running():
        st.session_state.status = "Offline"
        start_ollama()
    else:
        st.session_state.status = "Online"
        models = list_installed_models()  
    
if st.session_state.status == "Online":
    status.success("Ollama is running")
    


# Navigation Bar
pg = st.navigation({
    "DATA": [HomePage, StatsPage],
    "Tools": [ChatPage, PlotsPage],
    "About": [AboutPage]
}
)

if "df" not in st.session_state:
    st.session_state.df = None
if "file" not in st.session_state:
    st.session_state.file = None  

with st.sidebar:
    uploaded_file = st.file_uploader("Upload a data file", type=["csv", "xlsx", "xls", "json", "txt", "tsv", "parquet"])

    if uploaded_file is not None:
        import pandas as pd
        from pathlib import Path

        file_suffix = Path(uploaded_file.name).suffix.lower()
        try:
            with st.spinner("Loading..."):
                if file_suffix == ".csv":
                    df = pd.read_csv(uploaded_file)
                elif file_suffix in [".xlsx", ".xls"]:
                    df = pd.read_excel(uploaded_file)
                elif file_suffix == ".json":
                    df = pd.read_json(uploaded_file)
                elif file_suffix in [".txt", ".tsv"]:
                    df = pd.read_csv(uploaded_file, delimiter="\t")
                elif file_suffix == ".parquet":
                    df = pd.read_parquet(uploaded_file)
                else:
                    st.error("Unsupported file format")
                    df = None

                if df is not None:
                    st.session_state.df = df
                    st.session_state.file = uploaded_file

        except Exception as e:
            st.error(f"Failed to read file: {e}")


st.logo("assets/logo.png", size='medium')
with st.sidebar:
    st.caption("Support me by clicking on this button 👇")
    button(username="astrayn", floating=False, width=221)
    st.caption('0.0.3')


pg.run()