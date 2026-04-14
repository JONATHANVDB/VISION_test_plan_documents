import sys
import os
from PyPDF2 import PdfReader

def extract_pdf_first_pages(file_path, num_pages=3):
    out_file = file_path + ".txt"
    try:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"\n--- Extracting from {file_path} ---\n")
            reader = PdfReader(file_path)
            for i in range(min(num_pages, len(reader.pages))):
                page = reader.pages[i]
                text = page.extract_text()
                f.write(f"Page {i+1}:\n")
                f.write(text + "\n")
                f.write("-" * 40 + "\n")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    files = [
        "VISION_test_plan_documents/datasheets/MAG-CXP00002-NP_Datasheet_2025_11-rev2.1.pdf",
        "VISION_test_plan_documents/datasheets/MAG-IMG002X1-NC_Datasheet_2025_12-rev1.2.pdf",
        "VISION_test_plan_documents/datasheets/MAG-PSU00001-NP_Datasheet_2025_05-rev0.5.pdf",
        "VISION_test_plan_documents/datasheets/MAG-VIS100xx-N_Datasheet_2025_11-rev1.1.pdf"
    ]
    for f in files:
        extract_pdf_first_pages(f)
