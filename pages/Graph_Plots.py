import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df
    st.header("Plot Configuration")

    plot_type = st.selectbox(
        "Select Plot Type",
        ["Scatter Plot", "Line Plot", "Bar Chart", "Histogram", "Box Plot", "Heatmap", "Pie Chart"]
    )

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    all_cols = df.columns.tolist()
    
    # Main plotting area
    st.header(f"{plot_type} Generator")
    
    if plot_type == "Scatter Plot":
        st1, st2, st3 = st.columns([1, 1, 1])
        x_col = st1.selectbox("Select X-axis column", all_cols)
        y_col = st2.selectbox("Select Y-axis column", numeric_cols)
        color_col = st3.selectbox("Select color column (optional)", ["None"] + all_cols)
        
        if st.button("Generate Scatter Plot"):
            st.subheader("Scatter Plot")
            if color_col == "None":
                fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
            else:
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col} colored by {color_col}")
            st.plotly_chart(fig, use_container_width=True)
    
    elif plot_type == "Line Plot":
        st1, st2= st.columns([1, 1])
        x_col = st1.selectbox("Select X-axis column", all_cols)
        y_cols = st2.multiselect("Select Y-axis column(s)", numeric_cols)
        
        if st.button("Generate Line Plot"):
            if y_cols:
                st.subheader("Line Plot")
                fig = go.Figure()
                for y_col in y_cols:
                    fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines', name=y_col))
                fig.update_layout(title=f"Line Plot of {', '.join(y_cols)} vs {x_col}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Please select at least one Y-axis column.")
    
    elif plot_type == "Bar Chart":
        st1, st2, st3 = st.columns([1, 1, 1])
        x_col = st1.selectbox("Select X-axis column", all_cols)
        y_col = st2.selectbox("Select Y-axis column", numeric_cols)
        orientation = st3.radio("Orientation", ["Vertical", "Horizontal"])
        
        if st.button("Generate Bar Chart"):
            st.subheader("Bar Chart")
            if orientation == "Vertical":
                fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart of {y_col} vs {x_col}")
            else:
                fig = px.bar(df, y=x_col, x=y_col, title=f"Bar Chart of {y_col} vs {x_col}", orientation='h')
            st.plotly_chart(fig, use_container_width=True)
    
    elif plot_type == "Histogram":
        st1, st2 = st.columns([1, 1])
        hist_col = st1.selectbox("Select column for histogram", numeric_cols)
        bins = st2.slider("Number of bins", min_value=5, max_value=100, value=30)
        
        if st.button("Generate Histogram"):
            st.subheader("Histogram")
            fig = px.histogram(df, x=hist_col, nbins=bins, title=f"Histogram of {hist_col}")
            st.plotly_chart(fig, use_container_width=True)
    
    elif plot_type == "Box Plot":
        st1, st2 = st.columns([1, 1])
        y_col = st1.selectbox("Select column for values", numeric_cols)
        x_col = st2.selectbox("Select column for categories (optional)", ["None"] + all_cols)
        
        if st.button("Generate Box Plot"):
            st.subheader("Box Plot")
            if x_col == "None":
                fig = px.box(df, y=y_col, title=f"Box Plot of {y_col}")
            else:
                fig = px.box(df, x=x_col, y=y_col, title=f"Box Plot of {y_col} grouped by {x_col}")
            st.plotly_chart(fig, use_container_width=True)
    
    elif plot_type == "Heatmap":
        corr_method = st.selectbox("Correlation method", ["pearson", "spearman", "kendall"])
        
        if st.button("Generate Heatmap"):
            st.subheader("Correlation Heatmap")
            # Calculate correlation matrix
            corr_df = df[numeric_cols].corr(method=corr_method)
            
            fig = px.imshow(
                corr_df,
                text_auto=True,
                color_continuous_scale="RdBu_r",
                title=f"{corr_method.capitalize()} Correlation Heatmap"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif plot_type == "Pie Chart":
        st1, st2 = st.columns([1, 1])
        label_col = st1.selectbox("Select column for labels", all_cols)
        value_col = st2.selectbox("Select column for values", numeric_cols)
        
        if st.button("Generate Pie Chart"):
            st.subheader("Pie Chart")
            # Group data if needed
            if len(df[label_col].unique()) > 10:
                st.warning(f"Many unique values in {label_col} (>{len(df[label_col].unique())}). Consider using a different column.")
            
            grouped_data = df.groupby(label_col)[value_col].sum().reset_index()
            fig = px.pie(grouped_data, names=label_col, values=value_col, title=f"Pie Chart of {value_col} by {label_col}")
            st.plotly_chart(fig, use_container_width=True)
    
    # Download plotly figure as HTML
    if "fig" in locals():
        buffer = io.StringIO()
        fig.write_html(buffer)
        html_bytes = buffer.getvalue().encode()
        
        st.download_button(
            label="Download Plot as HTML",
            data=html_bytes,
            file_name=f"{plot_type.lower().replace(' ', '_')}.html",
            mime="text/html"
        )
else:
    st.markdown(f'''
                ### 📊 Interactive Graph Builder

Create beautiful, customizable plots from your dataset — no coding required!

#### 🎨 Supported Plots:
- Scatter Plot
- Line Plot
- Bar Chart (Vertical/Horizontal)
- Histogram
- Box Plot
- Correlation Heatmap
- Pie Chart

🛠️ Features:
- Dynamic column selection
- Plot customization options
- Download your charts as HTML

> **To get started:** Upload a CSV file on the main page or data overview tab.

📁 *Once uploaded, return here to start visualizing!*
''')
    st.warning("Upload a file to get started.")