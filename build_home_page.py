import os
import json

base_dir = r"d:\study material\projects\clinical_trial_termination_analysis\dashboard.Report\definition\pages"

def write_visual(page_folder, visual_name, visual_container_dict):
    v_dir = os.path.join(page_folder, "visuals", visual_name)
    os.makedirs(v_dir, exist_ok=True)
    with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as f:
        json.dump(visual_container_dict, f, indent=2)

def build_home_page():
    p_home = os.path.join(base_dir, "page_home_001")
    os.makedirs(os.path.join(p_home, "visuals"), exist_ok=True)

    # 1. Header Background Shape (Black, #111111)
    header_bg = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": "home_header_bg",
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
    write_visual(p_home, "home_header_bg", header_bg)

    # 2. Header Text (TRIALSCOPE branding)
    header_text = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": "home_header_text",
        "position": {"x": 32, "y": 14, "z": 1000, "height": 40, "width": 1856, "tabOrder": 1000},
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [{
                    "properties": {
                        "paragraphs": [{
                            "textRuns": [
                                {
                                    "value": "TRIALSCOPE",
                                    "textStyle": {"fontWeight": "bold", "fontSize": "16pt", "color": "#E89522"}
                                },
                                {
                                    "value": "   |   Clinical Trial Portfolio Dashboard",
                                    "textStyle": {"fontSize": "14pt", "color": "#FFFFFF"}
                                }
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
    write_visual(p_home, "home_header_text", header_text)

    # 3. Page Title & Mission Statement
    title_text = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": "home_title_text",
        "position": {"x": 32, "y": 96, "z": 2000, "height": 110, "width": 1856, "tabOrder": 2000},
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [{
                    "properties": {
                        "paragraphs": [
                            {
                                "textRuns": [{
                                    "value": "Clinical Trials at a Glance",
                                    "textStyle": {"fontWeight": "bold", "fontSize": "24pt", "color": "#15233A"}
                                }]
                            },
                            {
                                "textRuns": [{
                                    "value": "A focused view of trial completion, termination patterns and portfolio concentration across sponsors, phases, countries and conditions.",
                                    "textStyle": {"fontSize": "13pt", "color": "#687386"}
                                }]
                            }
                        ]
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
    write_visual(p_home, "home_title_text", title_text)

    # 4. KPI Card 1: Total Trials
    kpi1 = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": "home_kpi_total",
        "position": {"x": 32, "y": 230, "z": 3000, "height": 140, "width": 590, "tabOrder": 3000},
        "visual": {
            "visualType": "cardVisual",
            "query": {
                "queryState": {
                    "Data": {
                        "projections": [{
                            "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "fact_trials"}}, "Property": "Total Trials"}},
                            "queryRef": "fact_trials.Total Trials",
                            "nativeQueryRef": "Total Trials"
                        }]
                    }
                }
            },
            "objects": {
                "value": [{
                    "properties": {"labelDisplayUnits": {"expr": {"Literal": {"Value": "1D"}}}},
                    "selector": {"metadata": "fact_trials.Total Trials"}
                }]
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": "'Total Registered Trials (Finished)'"}}},
                        "alignment": {"expr": {"Literal": {"Value": "'center'"}}}
                    }
                }]
            },
            "drillFilterOtherVisuals": True
        }
    }
    write_visual(p_home, "home_kpi_total", kpi1)

    # 5. KPI Card 2: Termination Rate
    kpi2 = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": "home_kpi_rate",
        "position": {"x": 665, "y": 230, "z": 3100, "height": 140, "width": 590, "tabOrder": 3100},
        "visual": {
            "visualType": "cardVisual",
            "query": {
                "queryState": {
                    "Data": {
                        "projections": [{
                            "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "fact_trials"}}, "Property": "Termination Rate"}},
                            "queryRef": "fact_trials.Termination Rate",
                            "nativeQueryRef": "Termination Rate"
                        }]
                    }
                }
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": "'Portfolio Termination Rate'"}}},
                        "alignment": {"expr": {"Literal": {"Value": "'center'"}}}
                    }
                }]
            },
            "drillFilterOtherVisuals": True
        }
    }
    write_visual(p_home, "home_kpi_rate", kpi2)

    # 6. KPI Card 3: Median Enrollment
    kpi3 = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": "home_kpi_enroll",
        "position": {"x": 1298, "y": 230, "z": 3200, "height": 140, "width": 590, "tabOrder": 3200},
        "visual": {
            "visualType": "cardVisual",
            "query": {
                "queryState": {
                    "Data": {
                        "projections": [{
                            "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "fact_trials"}}, "Property": "Median Enrollment"}},
                            "queryRef": "fact_trials.Median Enrollment",
                            "nativeQueryRef": "Median Enrollment"
                        }]
                    }
                }
            },
            "objects": {
                "value": [{
                    "properties": {"labelDisplayUnits": {"expr": {"Literal": {"Value": "1D"}}}},
                    "selector": {"metadata": "fact_trials.Median Enrollment"}
                }]
            },
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": "'Median Enrollment per Trial'"}}},
                        "alignment": {"expr": {"Literal": {"Value": "'center'"}}}
                    }
                }]
            },
            "drillFilterOtherVisuals": True
        }
    }
    write_visual(p_home, "home_kpi_enroll", kpi3)

    # 7. Portfolio Snapshot Note Box
    snapshot_note = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": "home_snapshot_note",
        "position": {"x": 32, "y": 395, "z": 4000, "height": 135, "width": 1856, "tabOrder": 4000},
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [{
                    "properties": {
                        "paragraphs": [
                            {
                                "textRuns": [
                                    {"value": "Portfolio Snapshot & Methodology: ", "textStyle": {"fontWeight": "bold", "fontSize": "13pt", "color": "#15233A"}},
                                    {"value": "Approximately 1 in 10 finished interventional trials (10.3%) stopped early. Median enrollment (50 participants) is used instead of the arithmetic mean (458) because 164 mega-trials (>100,000 subjects) heavily skew the average. Stated stop reasons are classified from free-text sponsor submissions using keyword matching rules. Explore detailed findings in the sections below.", "textStyle": {"fontSize": "12pt", "color": "#687386"}}
                                ]
                            }
                        ]
                    }
                }]
            },
            "visualContainerObjects": {
                "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]
            },
            "drillFilterOtherVisuals": True
        }
    }
    write_visual(p_home, "home_snapshot_note", snapshot_note)

    # 8. Navigation Cards (4 text cards for sections)
    nav_sections = [
        ("Executive Overview", "Portfolio scale, phase volumes, completion vs termination split, and historical termination rate trends from 1990 to 2025.", 32),
        ("Termination Reasons", "In-depth taxonomy of stop reasons: enrollment difficulty, business decisions, safety signals, and trials stopped per 100 finished studies.", 500),
        ("Sponsor & Phase Deep-Dive", "Cross-comparison of termination risk and study scale across sponsor classes (Industry, NIH, Other) and developmental phases.", 968),
        ("Geography & Conditions", "Global clinical trial footprint across 200+ countries, top terminated conditions, and intervention type performance.", 1436)
    ]

    z = 5000
    for title, desc, x_pos in nav_sections:
        v_card = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
            "name": f"home_nav_{z}",
            "position": {"x": x_pos, "y": 555, "z": z, "height": 320, "width": 452, "tabOrder": z},
            "visual": {
                "visualType": "textbox",
                "objects": {
                    "general": [{
                        "properties": {
                            "paragraphs": [
                                {
                                    "textRuns": [{"value": title, "textStyle": {"fontWeight": "bold", "fontSize": "16pt", "color": "#E89522"}}]
                                },
                                {
                                    "textRuns": [{"value": "\n\n" + desc, "textStyle": {"fontSize": "12pt", "color": "#687386"}}]
                                }
                            ]
                        }
                    }]
                },
                "visualContainerObjects": {
                    "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}],
                    "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]
                },
                "drillFilterOtherVisuals": True
            }
        }
        write_visual(p_home, f"home_nav_{z}", v_card)
        z += 100

    print("Home page built successfully!")

if __name__ == "__main__":
    build_home_page()

