import os
import cairosvg

out_dir = "Projects/VISION_test_plan_documents/vision-module-testing-diagrams"
files = [
    "IMG002x1_production_test_flow.svg",
    "IMG002x1_trim_test_flow.svg",
    "CXP00002_production_test_flow.svg",
    "PSU00001_production_test_flow.svg",
    "VIS100xx_production_test_flow.svg"
]

for f in files:
    svg_path = os.path.join(out_dir, f)
    png_path = os.path.join(out_dir, f.replace(".svg", ".png"))
    try:
        cairosvg.svg2png(url=svg_path, write_to=png_path)
        print(f"Converted {f} to PNG")
    except Exception as e:
        print(f"Failed to convert {f}: {e}")
