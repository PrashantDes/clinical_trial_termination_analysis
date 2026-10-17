import os
import json

base_dir = r"d:\study material\projects\clinical_trial_termination_analysis\dashboard.Report\definition\pages"
pages = [
    ("4c5d547d9e1a3a5231a8", "Executive Overview"),
    ("page_reasons_b2a1", "Termination Reasons"),
    ("page_sponsor_c3b2", "Sponsor & Phase Deep-Dive"),
    ("page_geo_d4c3", "Geography & Conditions"),
    ("ce451a336be922af1920", "Data Notes")
]

for p_folder, p_name in pages:
    v_dir = os.path.join(base_dir, p_folder, "visuals")
    os.makedirs(v_dir, exist_ok=True)
    
    # 1. Header background shape (black #111111, height 64)
    h_bg = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": "global_header_bg",
        "position": {"x": 0, "y": 0, "z": 0, "height": 64, "width": 1920, "tabOrder": 0},
        "visual": {
            "visualType": "shape",
            "objects": {
                "shape": [{"properties": {"tileShape": {"expr": {"Literal": {"Value": "'rectangle'"}}}}}],
                "fill": [{"properties": {"fillColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#111111'"}}}}}}}]
            },
            "drillFilterOtherVisuals": True
        }
    }
    
    # 2. Header text with TRIALSCOPE branding and active page title
    h_text = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": "global_header_text",
        "position": {"x": 32, "y": 14, "z": 9000, "height": 40, "width": 1856, "tabOrder": 9000},
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [{
                    "properties": {
                        "paragraphs": [{
                            "textRuns": [
                                {"value": "TRIALSCOPE", "textStyle": {"fontWeight": "bold", "fontSize": "16pt", "color": "#E89522"}},
                                {"value": "   |   " + p_name, "textStyle": {"fontSize": "14pt", "color": "#FFFFFF"}}
                            ]
                        }]
                    }
                }]
            },
            "visualContainerObjects": {
                "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}],
                "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
            },
            "drillFilterOtherVisuals": True
        }
    }
    
    d1 = os.path.join(v_dir, "global_header_bg")
    os.makedirs(d1, exist_ok=True)
    with open(os.path.join(d1, "visual.json"), "w", encoding="utf-8") as f:
        json.dump(h_bg, f, indent=2)

    d2 = os.path.join(v_dir, "global_header_text")
    os.makedirs(d2, exist_ok=True)
    with open(os.path.join(d2, "visual.json"), "w", encoding="utf-8") as f:
        json.dump(h_text, f, indent=2)

print("Global headers applied across all pages successfully!")

