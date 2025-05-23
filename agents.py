# agents.py

from parse_excel import extract_quarter, is_valid
from pdf_writer import generate_pdf
from llm_writer import generate_batch_paragraphs

class ReportAgent:
    def __init__(self):
        self.df = None
        self.report_data = {}

    def load_dataframe(self, df):
        self.df = df

    def prepare_data(self, title_col, content_cols):
        from collections import defaultdict
        result = defaultdict(list)

        for _, row in self.df.iterrows():
            quarter = extract_quarter(row)
            if quarter not in ["Q1", "Q2", "Q3", "Q4"]:
                continue

            title = str(row.get(title_col, "")).strip()
            content = " ".join(
                str(row.get(col, "")).strip()
                for col in content_cols
                if is_valid(row.get(col))
            )

            if is_valid(title) and is_valid(content):
                result[quarter].append({
                    "section_title": title,
                    "content": content
                })

        self.report_data = dict(result)

    def generate_quarter_pdf(self, selected_quarter, user_prompt):
        if not self.report_data or selected_quarter not in self.report_data:
            return None, "Missing or invalid report data."

        try:
            entries = self.report_data[selected_quarter]
            rewritten_sections = {}

            for i in range(0, len(entries), 5):
                batch = entries[i:i + 5]
                batch_result = generate_batch_paragraphs(batch, user_prompt)
                rewritten_sections.update(batch_result)

            if not rewritten_sections:
                return None, "No valid sections generated."

            return generate_pdf(rewritten_sections, selected_quarter), "PDF generated successfully."
        except Exception as e:
            return None, f"Error generating PDF: {str(e)}"

    def generate_quarter_text(self, selected_quarter, user_prompt):
        if not self.report_data or selected_quarter not in self.report_data:
            return None, "Missing or invalid report data."

        try:
            entries = self.report_data[selected_quarter]
            rewritten_sections = {}

            for i in range(0, len(entries), 5):
                batch = entries[i:i + 5]
                batch_result = generate_batch_paragraphs(batch, user_prompt)
                rewritten_sections.update(batch_result)

            if not rewritten_sections:
                return None, "No valid sections generated."

            full_report = "\n\n".join(
                f"### {title}\n{paragraph}" for title, paragraph in rewritten_sections.items()
            )
            return full_report, "Text report generated successfully."
        except Exception as e:
            return None, f"Error generating report: {str(e)}"
