# app.py
    
import streamlit as st
from agents import ReportAgent

# Configure Streamlit page
st.set_page_config(page_title="Quarterly Report Generator", layout="centered")
st.title("Excel to Quarterly PDF Report Generator")

# --- Persist agent in session ---
if "agent" not in st.session_state:
    st.session_state.agent = ReportAgent()

agent = st.session_state.agent

# --- File Upload ---
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    with st.spinner("Parsing Excel file..."):
        parse_status = agent.ingest_excel(uploaded_file)
    if "successfully" in parse_status:
        st.success(parse_status)
    else:
        st.error(parse_status)

    # --- Quarter selection ---
    quarter = st.selectbox("Select Quarter to Generate", ["Q1", "Q2", "Q3", "Q4"])

    # --- Generate button ---
    if st.button("Generate PDF for Selected Quarter"):
        with st.spinner("Generating PDF..."):
            pdf_stream, message = agent.generate_quarter_pdf(quarter)
            if pdf_stream:
                st.success(message)
                st.download_button(
                    label=f"Download {quarter} Report",
                    data=pdf_stream,
                    file_name=f"{quarter}_Report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error(message)
