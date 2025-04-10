import streamlit as st
import pandas as pd
import numpy as np

st.session_state['stats'] = False
@st.cache_data
def display_comprehensive_stats(df):
    # Basic description statistics
    st.markdown("## Descriptive Statistics")
    st.write("### Basic Summary Statistics")
    st.write(df.describe())
    
    # Detailed column-wise statistics
    st.markdown("## Detailed Column Statistics")
    
    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.markdown("### Numeric Columns Analysis")
        
        # Detailed numeric column stats
        numeric_stats = pd.DataFrame({
            'Unique Count': df[numeric_cols].nunique(),
            'Missing Count': df[numeric_cols].isnull().sum(),
            'Missing Percentage': (df[numeric_cols].isnull().sum() / len(df) * 100).round(2),
            'Missing count': df.isnull().sum(),
            'Mean': df[numeric_cols].mean(),
            'Median': df[numeric_cols].median(),
            'Standard Deviation': df[numeric_cols].std(),
            'Skewness': df[numeric_cols].skew(),
            'Kurtosis': df[numeric_cols].kurtosis(),
            'Min': df[numeric_cols].min(),
            'Max': df[numeric_cols].max(),
            'Range': df[numeric_cols].max() - df[numeric_cols].min()
        })
        st.write(numeric_stats)
        
        # Correlation matrix for numeric columns
        st.markdown("### Correlation Matrix")
        correlation_matrix = df[numeric_cols].corr()
        st.write(correlation_matrix)
    
    # Categorical columns analysis
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        st.markdown("### Categorical Columns Analysis")
        
        # Categorical column stats
        categorical_stats = pd.DataFrame({
            'Unique Count': df[categorical_cols].nunique(),
            'Missing Count': df[categorical_cols].isnull().sum(),
            'Missing Percentage': (df[categorical_cols].isnull().sum() / len(df) * 100).round(2),
            'Most Frequent Value': df[categorical_cols].mode().iloc[0],
            'Value Counts': df[categorical_cols].apply(lambda x: x.value_counts().to_dict())
        })
        st.write(categorical_stats)
    
    # Additional DataFrame-level information
    st.markdown("## DataFrame Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### DataFrame Shape")
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")
    
    with col2:
        st.markdown("### Data Types")
        st.write(df.dtypes)
    
    # Memory usage
    st.markdown("### Memory Usage")
    st.write(f"Total Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")


if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df
    st.markdown("## Statistics")
    display_comprehensive_stats(df)
else:
    st.warning("Upload a file to get started.")
