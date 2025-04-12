import streamlit as st
import ollama

@st.cache_data
def callOllama(prompt, model="gemma3"):
    #Call the Ollama API with the given prompt.
    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.get('message', {}).get('content', "No response.")

@st.cache_data
def question():
    prompt = f"""Based on the following info extracted from a data set, write intersting questions 
    a data analyst can plot, present your output only in the following format:
    ['Question1', 'Question2', 'Question3']
    also do not use apostropes in the output.
    eg: ['What is the average age of customers?', 'How many unique products are sold?']
    
    Data Name: {st.session_state.file.name}
    Columns: {st.session_state.df.columns.tolist()} """
    response = callOllama(prompt, model="gemma3")
    return response
