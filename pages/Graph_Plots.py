import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def plot_graph(df, x_column, y_column, plot_type, title, x_label, y_label):
    """
    Create a graph based on user selections
    """
    plt.figure(figsize=(10, 6))
    # Different plot types
    if plot_type == 'Line Plot':
        plt.plot(df[x_column], df[y_column])
    elif plot_type == 'Scatter Plot':
        plt.scatter(df[x_column], df[y_column])
    elif plot_type == 'Bar Plot':
        plt.bar(df[x_column], df[y_column])
    elif plot_type == 'Histogram':
        plt.hist(df[y_column], bins='auto')
        x_label = 'Frequency'
    elif plot_type == 'Box Plot':
        sns.boxplot(x=df[x_column], y=df[y_column])
    
    # Customization
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    
    return plt

def main():
    st.title('Graph Plotter')
    if st.session_state.df is not None:
        df = st.session_state.df
        # Sidebar for plot configuration
        st.sidebar.header('Plot Configuration')
        
        # Column selection
        columns = df.columns.tolist()
        x_column = st.sidebar.selectbox('X-axis Column', columns)
        y_column = st.sidebar.selectbox('Y-axis Column', columns)
        
        # Plot type selection
        plot_types = [
            'Line Plot', 
            'Scatter Plot', 
            'Bar Plot', 
            'Histogram', 
            'Box Plot'
        ]
        plot_type = st.sidebar.selectbox('Plot Type', plot_types)
        
        # Additional customization
        title = st.sidebar.text_input('Plot Title', 'My Graph')
        x_label = st.sidebar.text_input('X-axis Label', x_column)
        y_label = st.sidebar.text_input('Y-axis Label', y_column)
        
        # Plot button
        if st.sidebar.button('Generate Plot'):
            try:
                # Create plot
                fig = plot_graph(
                    df, 
                    x_column, 
                    y_column, 
                    plot_type, 
                    title, 
                    x_label, 
                    y_label
                )
                
                # Display plot
                st.pyplot(fig)
                
                # Save plot button
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                
                st.download_button(
                    label='Download Plot',
                    data=buf,
                    file_name=f'{title}.png',
                    mime='image/png'
                )
            
            except Exception as e:
                st.error(f"Error generating plot: {e}")
    else:
        st.write('Please upload a file to get started.')

if __name__ == '__main__':
    main()