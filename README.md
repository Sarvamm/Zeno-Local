#  DATARS – Automated Data Analysis

DATARS is a powerful and user-friendly Streamlit app that leverages local LLMs to understand, summarize, and visualize your dataset—all in a few clicks. Whether you're an analyst or a data science enthusiast, DATARS helps you interact with your data like never before.

---

## Features

###  1. Data Overview Page
Harness the power of AI to:
- Summarize your dataset automatically
- Detect outliers
- Perform correlation analysis
- Recommend and generate suitable graphs using LLMs
![Data Overview](https://raw.githubusercontent.com/Sarvamm/DATARS---Automated-Data-Analysis/refs/heads/main/assets/overview.png)

###  2. Data Profiling Page
Get a comprehensive EDA report powered by ydata_profiling, including:
- **Warnings**: Spot potential issues (missing values, skewness, etc.)
- **Univariate Analysis**: Summary stats (mean, median, mode) and histograms
- **Multivariate Analysis**: Correlation heatmaps, missing data patterns, duplicate detection, and pairwise relationships
![Data Profiling](https://raw.githubusercontent.com/Sarvamm/DATARS---Automated-Data-Analysis/refs/heads/main/assets/profiling.png)

###  3. Chatbot
Type in natural language commands like:
> “Plot the distribution of column A”  
> “Show mean values grouped by category”  
> “Detect missing values”

LLM-backed chatbot will convert it into Python code, run it, and show you the result—instantly.
![Talk to Tars](https://raw.githubusercontent.com/Sarvamm/DATARS---Automated-Data-Analysis/refs/heads/main/assets/chatbot.png)

### 📈 4. Manual Graph Plotter
If you want to customize visualizations yourself, use the dedicated graph plotter to manually create a wide variety of plots.
![Plot Graphs](https://raw.githubusercontent.com/Sarvamm/DATARS---Automated-Data-Analysis/refs/heads/main/assets/graphplotter.png)
---

## 🧰 Tech Stack & Libraries

- [Streamlit](https://streamlit.io/) 
- [Ollama](https://ollama.com/) 
- [Pandas](https://pandas.pydata.org/) 
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/) 
- [Plotly](https://plotly.com/python/) 
- [YData Profiling](https://github.com/ydataai/ydata-profiling) 
- [streamlit-extras](https://github.com/arnaudmiribel/streamlit-extras)
- [streamlit-pandas-profiling](https://github.com/pandas-profiling/pandas-profiling)

---

##  Getting Started

###  Installation
```bash
git clone https://github.com/sarvamm/DATARS---Automated-Data-Analysis.git
cd DATARS---Automated-Data-Analysis
pip install -r requirements.txt
```

###  Set Up Ollama
Ensure Ollama and your preferred local LLM are installed and running.
By default gemma3 and qwen2.5-coder:7b are used so make sure you have them.

### Install Ollama
```bash
pip install ollama
```

### Install gemma3 and qwen2.5-coder:7b
```bash
ollama pull gemma3
```
```bash
ollama pull qwen2.5-coder:7b
```
---

## Run the App
```bash
streamlit run App.py
```

---

## Folder Structure
```
DATARS/
│
├── App.py                     # Main entry point
├── Functions.py               # Helper functions
├── .streamlit/                # Config and secrets
├── pages/
│   ├── About.py
│   ├── Chatbot.py
│   ├── Graph_Plots.py
│   ├── Overview.py
│   └── Statistics.py
├── assets/                    # Logo and media
├── outputs/                   # Generated reports
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

##  License

This project is licensed under the terms of the Non-Profit Open Software License version 3.0.