import os

def create_flow_svg(filename, title, steps):
    svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{150 + len(steps)*80}" viewBox="0 0 800 {150 + len(steps)*80}" style="display:block;width:800px;height:{150 + len(steps)*80}px">
  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2f3f5c" />
    </marker>
  </defs>
  <rect width="800" height="{150 + len(steps)*80}" fill="#fafbfc" />
  <text x="400" y="40" style="font-weight:600;font-size:24px;font-family:'Segoe UI', 'Helvetica Neue', Arial, sans-serif;text-anchor:middle;fill:#1a2332">{title}</text>
'''
    y = 80
    for i, step in enumerate(steps):
        svg += f'''
  <rect x="250" y="{y}" width="300" height="50" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" />
  <text x="400" y="{y + 30}" style="font-weight:700;font-size:14px;font-family:'Segoe UI', 'Helvetica Neue', Arial, sans-serif;text-anchor:middle;fill:#2f3f5c">{step}</text>
'''
        if i < len(steps) - 1:
            svg += f'''
  <line x1="400" y1="{y + 50}" x2="400" y2="{y + 80}" stroke="#2f3f5c" stroke-width="2.5" marker-end="url(#a)" />
'''
        y += 80

    svg += '</svg>'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)

out_dir = "Projects/VISION_test_plan_documents/vision-module-testing-diagrams"

create_flow_svg(f"{out_dir}/IMG002x1_production_test_flow.svg", "MAG-IMG002x1-NC Production Test Flow", ["Visual Inspection (VI)", "Connectivity Test (CONN)", "Final Test (FT)"])
create_flow_svg(f"{out_dir}/IMG002x1_trim_test_flow.svg", "MAG-IMG002x1-NC Trim Test Flow", ["Connectivity Test (CONN)", "Trimming (TRIM)"])
create_flow_svg(f"{out_dir}/CXP00002_production_test_flow.svg", "MAG-CXP00002-NP Production Test Flow", ["Visual Inspection (VI)", "Connectivity Test (CONN)", "Final Test (FT)"])
create_flow_svg(f"{out_dir}/PSU00001_production_test_flow.svg", "MAG-PSU00001-NP Production Test Flow", ["Visual Inspection (VI)", "Connectivity Test (CONN)", "Final Test (FT)"])
create_flow_svg(f"{out_dir}/VIS100xx_production_test_flow.svg", "MAG-VIS100xx-N Production Test Flow", ["Visual Inspection (VI)", "Connectivity Test (CONN)", "Module Final Test (FT)"])

print("SVGs generated.")
