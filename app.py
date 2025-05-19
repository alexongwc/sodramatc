# app.py
    
import streamlit as st
from agents import ReportAgent

# Configure Streamlit page
st.set_page_config(page_title="Quarterly Report Generator", layout="centered")
st.title("Excel to Quarterly Report Generator")

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

    # --- Prompt input area ---
    default_prompt = """You are a professional report writer preparing a government-style quarterly report.

For each numbered item below:
1. Rephrase the title as a single polished sentence (this will be the bold+underlined heading)
2. Rewrite the content into a concise, human-sounding paragraph suitable for reporting
3. If the content is incoherent, vague, empty, or includes phrases like "test", "lorem", "in this quarter", or any generic filler text, **DO NOT fabricate a paragraph**. Instead, respond with "[SKIP: Incoherent or insufficient content]".

Be truthful and do not make up information."""
    user_prompt = st.text_area("Customize your prompt if needed:", value=default_prompt, height=300)
    st.session_state.user_prompt = user_prompt

    # --- Quarter selection ---
    quarter = st.selectbox("Select Quarter to Generate", ["Q1", "Q2", "Q3", "Q4"])

    # --- Output Mode Toggle ---
    output_mode = st.radio("Choose Output Format", ["PDF", "Plain Text"])

    # --- Generate button ---
    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            if output_mode == "PDF":
                pdf_stream, message = agent.generate_quarter_pdf(quarter, user_prompt)
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
            else:
                report_text, message = agent.generate_quarter_text(quarter, user_prompt)
                if report_text:
                    st.success(message)
                    st.text_area("Generated Report:", value=report_text, height=600)
                else:
                    st.error(message)
