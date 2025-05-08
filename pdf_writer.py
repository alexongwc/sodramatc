# pdf_writer.py

from fpdf import FPDF
from io import BytesIO

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font("Arial", size=12)

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_title(self, title):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, title, ln=True, align="C")
        self.ln(5)

    def add_section(self, title, paragraph):
        # Clean non-ASCII characters
        title = title.encode("ascii", "ignore").decode()
        paragraph = paragraph.encode("ascii", "ignore").decode()

        # Bold + underline for the title
        self.set_font("Arial", "BU", 12)
        self.multi_cell(0, 8, title)
        self.ln(1)

        # Regular body text
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 8, paragraph)
        self.ln(5)

def generate_pdf(rewritten_sections: dict, quarter: str) -> BytesIO:
    pdf = PDF()
    pdf.add_title(f"{quarter} Progress Report")

    for title, paragraph in rewritten_sections.items():
        if "[ERROR" in paragraph:
            continue
        pdf.add_section(title, paragraph)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer