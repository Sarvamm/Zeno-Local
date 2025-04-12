import streamlit as st


if 'report' not in st.session_state:
    st.session_state.report = None

def generate_report(df):
    if st.session_state.report is not None:
        st_profile_report(st.session_state.report)
    else:
        st.session_state.report = df.profile_report()
        st_profile_report(st.session_state.report)

    st.session_state.report.to_file("outputs/report.html")


if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df
    from ydata_profiling import ProfileReport
    from streamlit_pandas_profiling import st_profile_report
    from streamlit_extras.floating_button import floating_button
    generate_report(df)
    try:
        @st.dialog("Download Report")
        def download_report():
            st.download_button(
                label="Download Report",
                data=open("outputs/report.html", "r+"),
                file_name="report.html",
                mime="text/html"
            )

    except Exception as e:
        st.error(f"Error generating report: {e}")

    if floating_button("Download Report", icon="📥"):
        download_report()

else:
    st.markdown(f'''
                ### 📋 Data Profiler

Get a **detailed and automated report** of your dataset in just one click!

#### 🔍 What you'll get:
- Variable types & distributions
- Missing value analysis
- Correlations & duplicates
- Interactive visualizations
- Downloadable HTML report

⚡ Powered by **YData Profiling** and built for **quick insights**.

> **To begin:** Upload a CSV file on the main page or data overview tab.

📁 *Once uploaded, come back here to generate your report!*

                ''')
    st.warning("Upload a file to get started.")
