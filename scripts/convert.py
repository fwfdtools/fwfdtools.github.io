import fitz  # PyMuPDF
import csv
import re

pdf_path = "forcelist.pdf"
csv_path = "data.csv"

doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text()

entries = re.findall(r"(\d+)\s+([A-Za-z,\.\s\(\)]+?)\s+Force Hire for the A\s+Shift\s+(.*?)(?=(\n\d+\s)|$)", text, re.DOTALL)

csv_rows = [("Number", "Name", "List", "Rank", "Opportunity Factors")]
for num, name, data, _ in entries:
    data_lines = list(filter(None, map(str.strip, data.split('\n'))))
    rank = data_lines[0] if data_lines else ""
    opportunity_factors = ", ".join(data_lines[1:]) if len(data_lines) > 1 else ""
    csv_rows.append((num, name.strip(), "Force Hire for the A", rank.strip(), opportunity_factors.strip()))

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(csv_rows)
