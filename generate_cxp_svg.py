import os

def create_cxp_flow_svg(filename):
    svg = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="650" viewBox="0 0 800 650" style="display:block;width:800px;height:650px">
  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2f3f5c" />
    </marker>
  </defs>
  <rect width="800" height="650" fill="#fafbfc" />
  <text x="400" y="40" style="font-weight:600;font-size:24px;font-family:'Segoe UI', 'Helvetica Neue', Arial, sans-serif;text-anchor:middle;fill:#1a2332">MAG-CXP00002-NP Production Test Flow</text>

  <!-- Node 1 -->
  <rect x="250" y="80" width="300" height="60" rx="30" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="2" />
  <text x="400" y="115" style="font-weight:700;font-size:14px;font-family:'Segoe UI', 'Helvetica Neue', Arial, sans-serif;text-anchor:middle;fill:#2f3f5c">Device assembly</text>
  <line x1="400" y1="140" x2="400" y2="180" stroke="#2f3f5c" stroke-width="2.5" marker-end="url(#a)" />

  <!-- Node 2 -->
  <rect x="250" y="180" width="300" height="70" rx="10" fill="#fffbeb" stroke="#fcd34d" stroke-width="2" />
  <text x="400" y="210" style="font-weight:700;font-size:14px;font-family:'Segoe UI', 'Helvetica Neue', Arial, sans-serif;text-anchor:middle;fill:#2f3f5c">
    <tspan x="400" dy="0">TRIM @ RT,</tspan>
    <tspan x="400" dy="1.2em">Vnom + write OTP</tspan>
  </text>
  <line x1="400" y1="250" x2="400" y2="290" stroke="#2f3f5c" stroke-width="2.5" marker-end="url(#a)" />

  <!-- Node 3 -->
  <rect x="250" y="290" width="300" height="60" rx="10" fill="#fffbeb" stroke="#fcd34d" stroke-width="2" />
  <text x="400" y="325" style="font-weight:700;font-size:14px;font-family:'Segoe UI', 'Helvetica Neue', Arial, sans-serif;text-anchor:middle;fill:#2f3f5c">FT</text>
  <line x1="400" y1="350" x2="400" y2="390" stroke="#2f3f5c" stroke-width="2.5" marker-end="url(#a)" />

  <!-- Node 4 -->
  <rect x="250" y="390" width="300" height="60" rx="10" fill="#fef2f2" stroke="#fca5a5" stroke-width="2" />
  <text x="400" y="425" style="font-weight:700;font-size:14px;font-family:'Segoe UI', 'Helvetica Neue', Arial, sans-serif;text-anchor:middle;fill:#2f3f5c">binning</text>
  <line x1="400" y1="450" x2="400" y2="490" stroke="#2f3f5c" stroke-width="2.5" marker-end="url(#a)" />

  <!-- Node 5 -->
  <rect x="250" y="490" width="300" height="60" rx="30" fill="#ecfdf5" stroke="#a7f3d0" stroke-width="2" />
  <text x="400" y="520" style="font-weight:700;font-size:14px;font-family:'Segoe UI', 'Helvetica Neue', Arial, sans-serif;text-anchor:middle;fill:#2f3f5c">
    <tspan x="400" dy="0">Packing and</tspan>
    <tspan x="400" dy="1.2em">Shipment</tspan>
  </text>
</svg>
'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)

out_dir = "Projects/VISION_test_plan_documents/vision-module-testing-diagrams"
create_cxp_flow_svg(f"{out_dir}/CXP00002_production_test_flow.svg")
print("CXP SVG generated.")
