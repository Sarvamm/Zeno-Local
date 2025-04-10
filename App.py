import streamlit as st
import pandas as pd
#Page setup
HomePage = st.Page(
    page="pages/Home.py",
    icon="🏠",
    title = "Home",
    default = True
)
StatsPage = st.Page(
    page="pages/Statistics.py",
    icon="📊",
    title = "Statistics"
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
ChatPage2 = st.Page(
    page="pages/CB2.py",
    icon="🤖",    
    title = "Chatbot2"
)

# Navigation Bar
pg = st.navigation({
    "DATA": [HomePage, StatsPage, ChatPage, ChatPage2],
    "Tools": [PlotsPage]
}
)

if "df" not in st.session_state:
    st.session_state.df = None
if "file" not in st.session_state:
    st.session_state.file = None  

with st.sidebar:
    uploaded_file = st.file_uploader("", type=["csv"])

    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.file = uploaded_file

st.logo("assets/logo2.png", size='large')

pg.run()