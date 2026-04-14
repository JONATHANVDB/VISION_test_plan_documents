import sys
import os
import docx

def extract_docx(file_path):
    out_file = file_path + ".txt"
    try:
        doc = docx.Document(file_path)
        with open(out_file, "w", encoding="utf-8") as f:
            for para in doc.paragraphs:
                if para.style.name.startswith('Heading'):
                    f.write(f"\n{para.style.name}: {para.text}\n")
                elif para.text.strip():
                    f.write(f"{para.text}\n")
    except Exception as e:
        print(f"Error reading docx: {e}")

if __name__ == "__main__":
    files = [
        "Projects/VISION_test_plan_documents/test plans/IMG002x1_test_plan_1v2.docx",
        "Projects/VISION_test_plan_documents/test plans/mag-cxp-product-test-plan_1v2.docx",
        "Projects/VISION_test_plan_documents/test plans/MAG_VIS100XX_EVK_Modules_Test_Plan.docx",
        "Projects/VISION_test_plan_documents/test plans/ProductTestDevelopmentMAG-PSU_test_plan_1v2.docx"
    ]
    for f in files:
        extract_docx(f)
