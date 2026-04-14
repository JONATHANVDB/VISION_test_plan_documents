import pandas as pd
import sys
import os

def extract_limits(file_path):
    out_file = file_path + ".txt"
    try:
        df = pd.read_excel(file_path)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"--- Limits from {file_path} ---\n")
            f.write(df.to_string())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    files = [
        "DCDC-tester-python-sw/dcdc_tester_python_sw/f_post_processing/check_limits.xlsx",
        "proxima-product-test-sw/proxima_product_test_sw/f_post_processing/check_limits.xlsx",
        "Vision-MEGACAM-python-sw/vision_megacam_python_sw/f_post_processing/check_limits.xlsx"
    ]
    for f in files:
        if os.path.exists(f):
            extract_limits(f)
        else:
            # try to find it
            for root, dirs, filenames in os.walk(f.split('/')[0]):
                for filename in filenames:
                    if filename == 'check_limits.xlsx':
                        extract_limits(os.path.join(root, filename))
