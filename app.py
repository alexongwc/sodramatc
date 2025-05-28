# app.py

import streamlit as st
import pandas as pd
from agents import ReportAgent

# Page config
st.set_page_config(page_title="Quarterly Report Generator", layout="centered")
st.title("SoDrama Excel Quarterly Report Generator")

# Instantiate agent
if "agent" not in st.session_state:
    st.session_state.agent = ReportAgent()

agent = st.session_state.agent

# Upload section
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Read and clean DataFrame
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    df.columns = df.columns.str.strip().str.replace(r"\s+", " ", regex=True)
    st.session_state.df = df
    agent.load_dataframe(df)

    st.success("Excel parsed successfully. Please select the relevant columns below.")

    # Column selection
    all_columns = df.columns.tolist()
    title_col = st.selectbox("Select the column to use as TITLE (1 only):", all_columns)
    paragraph_cols = st.multiselect("Select column(s) to use as PARAGRAPH CONTENT (up to 5):", all_columns, max_selections=5)

    if title_col and paragraph_cols:
        agent.prepare_data(title_col, paragraph_cols)

        # Prompt input
        default_prompt = """**ROLE**:  > You are a **professional high-fidelity condenser** specializing in **critical condensation** for government-style report. 
---
## Core Mission
You must condense complex documents context **without summarizing**, **without deleting key examples, tone, or causal logic**, while maintaining **logical flow** and **emotional resonance**.  

## Tone Retention
- Match original emotional and stylistic tone by genre.

## Fidelity Over Brevity Principle
- If shortening endangers meaning, logical scaffolding, or emotional tone — **retain longer form**.

Common Mistakes to Avoid:
- Logical causality collapse  
- Emotional flattening  
- Over-compression of technical precision  
- Tone mismatches  

## Final QA Checklist
- [ ] Main arguments preserved?  
- [ ] Key examples intact?  
- [ ] Emotional and logical tone maintained?  
- [ ] Logical flow unbroken?  
- [ ] No misinterpretation introduced?  


For each numbered item below:
1. Rephrase the title as a single polished sentence. Do not exceed 7 words (this will be the bold+underlined heading)
2. Rewrite the content into a concise, human-sounding paragraph suitable for reporting. Do not exceed 150 words. 
3. If the content is incoherent, vague, empty, or any generic filler text, **DO NOT fabricate a paragraph**. Instead, respond with "[SKIP: Incoherent or insufficient content]".

Be truthful and do not make up information."""
        user_prompt = st.text_area("Customize your prompt if needed:", value=default_prompt, height=300)

        # Quarter + Output mode
        quarter = st.selectbox("Select Quarter to Generate", ["Q1", "Q2", "Q3", "Q4"])
        output_mode = st.radio("Choose Output Format", ["PDF", "Plain Text"])

        # Generate
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
    else:
        st.warning("Please select a TITLE column and at least one PARAGRAPH column.")