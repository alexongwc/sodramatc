# agents.py

from parse_excel import parse_excel, is_valid
from pdf_writer import generate_pdf
from llm_writer import generate_batch_paragraphs

class ReportAgent:
    def __init__(self):
        self.report_data = None

    def ingest_excel(self, uploaded_file):
        try:
            self.report_data = parse_excel(uploaded_file)
            print("Parsed Quarters:", list(self.report_data.keys()))
            return "Excel parsed successfully."
        except Exception as e:
            return f"Failed to parse Excel: {str(e)}"

    def generate_quarter_pdf(self, selected_quarter):
        if not self.report_data or selected_quarter not in self.report_data:
            return None, "Missing or invalid report data."

        try:
            entries = self.report_data[selected_quarter]
            rewritten_sections = {}

            for i in range(0, len(entries), 5):
                batch = entries[i:i + 5]
                valid_batch = [
                    entry for entry in batch
                    if is_valid(entry.get("section_title")) and is_valid(entry.get("content"))
                ]
                if not valid_batch:
                    continue

                # 🔍 Debug: print what is being sent to GPT
                print("Sending batch to LLM:")
                for entry in valid_batch:
                    print(f"Title: {entry['section_title']}\nContent: {entry['content']}\n---")

                batch_result = generate_batch_paragraphs(valid_batch)

                # 🔍 Debug: print how many paragraphs returned
                print(f"GPT returned {len(batch_result)} paragraphs.\n")

                rewritten_sections.update(batch_result)

            if not rewritten_sections:
                return None, "No valid sections generated."

            pdf_stream = generate_pdf(rewritten_sections, selected_quarter)
            return pdf_stream, "PDF generated successfully."

        except Exception as e:
            return None, f"Error generating PDF: {str(e)}"
