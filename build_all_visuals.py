import os
import json

base_dir = r"d:\study material\projects\clinical_trial_termination_analysis\dashboard.Report\definition\pages"

def make_visual(page_folder, visual_name, x, y, width, height, z, visual_dict):
    v_dir = os.path.join(page_folder, "visuals", visual_name)
    os.makedirs(v_dir, exist_ok=True)
    vc = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": visual_name,
        "position": {
            "x": x,
            "y": y,
            "z": z,
            "height": height,
            "width": width,
            "tabOrder": z
        },
        "visual": visual_dict
    }
    with open(os.path.join(v_dir, "visual.json"), "w", encoding="utf-8") as f:
        json.dump(vc, f, indent=2)

def make_card(entity, measure_name, title_text=""):
    return {
        "visualType": "cardVisual",
        "query": {
            "queryState": {
                "Data": {
                    "projections": [{
                        "field": {
                            "Measure": {
                                "Expression": {"SourceRef": {"Entity": entity}},
                                "Property": measure_name
                            }
                        },
                        "queryRef": f"{entity}.{measure_name}",
                        "nativeQueryRef": measure_name
                    }]
                }
            }
        },
        "visualContainerObjects": {
            "title": [{
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "text": {"expr": {"Literal": {"Value": f"'{title_text or measure_name}'"}}},
                    "alignment": {"expr": {"Literal": {"Value": "'center'"}}}
                }
            }]
        },
        "drillFilterOtherVisuals": True
    }

def make_slicer(entity, col_name, display_name):
    return {
        "visualType": "slicer",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [{
                        "field": {
                            "Column": {
                                "Expression": {"SourceRef": {"Entity": entity}},
                                "Property": col_name
                            }
                        },
                        "queryRef": f"{entity}.{col_name}",
                        "nativeQueryRef": display_name,
                        "active": True,
                        "displayName": display_name
                    }]
                }
            }
        },
        "objects": {
            "data": [{"properties": {"mode": {"expr": {"Literal": {"Value": "'Dropdown'"}}}}}]
        },
        "drillFilterOtherVisuals": True
    }

def make_clustered_bar(entity, cat_col, measure_entity, measure_name, title_text, cat_display=""):
    return {
        "visualType": "clusteredBarChart",
        "query": {
            "queryState": {
                "Category": {
                    "projections": [{
                        "field": {
                            "Column": {
                                "Expression": {"SourceRef": {"Entity": entity}},
                                "Property": cat_col
                            }
                        },
                        "queryRef": f"{entity}.{cat_col}",
                        "nativeQueryRef": cat_display or cat_col,
                        "active": True
                    }]
                },
                "Y": {
                    "projections": [{
                        "field": {
                            "Measure": {
                                "Expression": {"SourceRef": {"Entity": measure_entity}},
                                "Property": measure_name
                            }
                        },
                        "queryRef": f"{measure_entity}.{measure_name}",
                        "nativeQueryRef": measure_name
                    }]
                }
            }
        },
        "visualContainerObjects": {
            "title": [{
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}}
                }
            }]
        },
        "drillFilterOtherVisuals": True
    }

def make_pivot_table(row_entity, row_col, val_entity, val_measures, title_text, col_entity=None, col_col=None):
    projections_val = [{
        "field": {
            "Measure": {
                "Expression": {"SourceRef": {"Entity": val_entity}},
                "Property": m
            }
        },
        "queryRef": f"{val_entity}.{m}",
        "nativeQueryRef": m
    } for m in val_measures]

    qs = {
        "Rows": {
            "projections": [{
                "field": {
                    "Column": {
                        "Expression": {"SourceRef": {"Entity": row_entity}},
                        "Property": row_col
                    }
                },
                "queryRef": f"{row_entity}.{row_col}",
                "nativeQueryRef": row_col,
                "active": True
            }]
        },
        "Values": {
            "projections": projections_val
        }
    }
    if col_entity and col_col:
        qs["Columns"] = {
            "projections": [{
                "field": {
                    "Column": {
                        "Expression": {"SourceRef": {"Entity": col_entity}},
                        "Property": col_col
                    }
                },
                "queryRef": f"{col_entity}.{col_col}",
                "nativeQueryRef": col_col,
                "active": True
            }]
        }
    return {
        "visualType": "pivotTable",
        "query": {"queryState": qs},
        "visualContainerObjects": {
            "title": [{
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "text": {"expr": {"Literal": {"Value": f"'{title_text}'"}}}
                }
            }]
        },
        "drillFilterOtherVisuals": True
    }


def build_page_1():
    p1 = os.path.join(base_dir, "4c5d547d9e1a3a5231a8")
    
    # 3 Top KPI Cards
    make_visual(p1, "p1_card_total", 30, 90, 370, 140, 1000, make_card("fact_trials", "Total Trials", "Total Trials"))
    make_visual(p1, "p1_card_term", 420, 90, 370, 140, 2000, make_card("fact_trials", "Terminated Trials", "Terminated Trials"))
    make_visual(p1, "p1_card_rate", 810, 90, 370, 140, 3000, make_card("fact_trials", "Termination Rate", "Termination Rate (%)"))
    
    # Slicers: Year, Phase
    make_visual(p1, "p1_slicer_year", 1210, 90, 330, 140, 4000, make_slicer("fact_trials", "start_year", "Start Year"))
    make_visual(p1, "p1_slicer_phase", 1560, 90, 330, 140, 5000, make_slicer("fact_trials", "phase", "Phase"))

    # Donut Chart: Completed vs Terminated
    donut_p1 = {
        "visualType": "donutChart",
        "query": {
            "queryState": {
                "Category": {
                    "projections": [{
                        "field": {"Column": {"Expression": {"SourceRef": {"Entity": "fact_trials"}}, "Property": "overall_status"}},
                        "queryRef": "fact_trials.overall_status",
                        "nativeQueryRef": "Status",
                        "active": True
                    }]
                },
                "Y": {
                    "projections": [{
                        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "fact_trials"}}, "Property": "Total Trials"}},
                        "queryRef": "fact_trials.Total Trials",
                        "nativeQueryRef": "Total Trials"
                    }]
                }
            }
        },
        "visualContainerObjects": {
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'Completed vs Terminated Split'"}}}}}]
        },
        "drillFilterOtherVisuals": True
    }
    make_visual(p1, "p1_donut_status", 1210, 250, 680, 400, 6000, donut_p1)

    # Clustered Bar: Phase vs Total Trials
    bar_p1 = make_clustered_bar("fact_trials", "phase", "fact_trials", "Total Trials", "Total Trials by Phase", "Phase")
    make_visual(p1, "p1_bar_phase", 30, 250, 1160, 400, 7000, bar_p1)

    # Line Chart: Trend Over Time
    line_p1 = {
        "visualType": "lineChart",
        "query": {
            "queryState": {
                "Category": {
                    "projections": [{
                        "field": {"Column": {"Expression": {"SourceRef": {"Entity": "fact_trials"}}, "Property": "start_year"}},
                        "queryRef": "fact_trials.start_year",
                        "nativeQueryRef": "Start Year",
                        "active": True
                    }]
                },
                "Y": {
                    "projections": [{
                        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "fact_trials"}}, "Property": "Termination Rate"}},
                        "queryRef": "fact_trials.Termination Rate",
                        "nativeQueryRef": "Termination Rate"
                    }]
                }
            }
        },
        "visualContainerObjects": {
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'Termination Rate Trend over Start Year'"}}}}}]
        },
        "drillFilterOtherVisuals": True
    }
    make_visual(p1, "p1_line_trend", 30, 670, 1860, 370, 8000, line_p1)
    print("Page 1 complete.")


def build_page_2():
    p2 = os.path.join(base_dir, "page_reasons_b2a1")

    # Stacked bar: Termination Reason counts
    bar_reasons = make_clustered_bar("fact_trials", "termination_reason", "fact_trials", "Terminated Trials", "Terminated Trials by Stop Reason", "Reason")
    make_visual(p2, "p2_bar_reasons", 30, 90, 700, 470, 1000, bar_reasons)

    # Slicers: Phase, Sponsor Group
    make_visual(p2, "p2_slicer_phase", 1540, 90, 350, 220, 2000, make_slicer("fact_trials", "phase", "Phase"))
    make_visual(p2, "p2_slicer_sponsor", 1540, 330, 350, 230, 3000, make_slicer("fact_trials", "sponsor_group", "Sponsor Group"))

    # Clustered Bar: Reasons per 100 Finished Trials
    bar_per100 = make_clustered_bar("fact_trials", "termination_reason", "fact_trials", "Terminated per 100", "Trials Stopped per 100 Finished Trials", "Reason")
    make_visual(p2, "p2_bar_per100", 750, 90, 770, 470, 4000, bar_per100)

    # Matrix: Reasons x Sponsor Group Cross-Tab
    matrix_reasons = make_pivot_table(
        "fact_trials", "termination_reason",
        "fact_trials", ["Terminated Trials", "Terminated per 100"],
        "Reason by Sponsor Group Cross-Tab",
        col_entity="fact_trials", col_col="sponsor_group"
    )
    make_visual(p2, "p2_matrix_crosstab", 30, 580, 1860, 460, 5000, matrix_reasons)
    print("Page 2 complete.")


def build_page_3():
    p3 = os.path.join(base_dir, "page_sponsor_c3b2")

    # Cards: Terminated Trials, Total Trials, Avg Enrollment
    make_visual(p3, "p3_card_term", 30, 90, 370, 140, 1000, make_card("fact_trials", "Terminated Trials", "Terminated Trials"))
    make_visual(p3, "p3_card_rate", 420, 90, 370, 140, 2000, make_card("fact_trials", "Termination Rate", "Termination Rate"))
    make_visual(p3, "p3_card_enroll", 810, 90, 370, 140, 3000, make_card("fact_trials", "Avg Enrollment", "Avg Enrollment per Trial"))
    
    # Slicer: Sponsor Class
    make_visual(p3, "p3_slicer_class", 1210, 90, 680, 140, 4000, make_slicer("fact_trials", "source_class", "Sponsor Class"))

    # Matrix: Sponsor Group x Phase
    matrix_sponsor = make_pivot_table(
        "fact_trials", "sponsor_group",
        "fact_trials", ["Total Trials", "Terminated Trials", "Termination Rate"],
        "Sponsor Group by Phase Breakdown",
        col_entity="fact_trials", col_col="phase"
    )
    make_visual(p3, "p3_matrix_sponsor", 30, 250, 1160, 410, 5000, matrix_sponsor)

    # Clustered Bar: Detailed Source Class Termination Rate
    bar_class = make_clustered_bar("fact_trials", "source_class", "fact_trials", "Termination Rate", "Termination Rate by Detailed Sponsor Class", "Class")
    make_visual(p3, "p3_bar_class", 1210, 250, 680, 410, 6000, bar_class)

    # Clustered Bar: Phase vs Avg Enrollment
    bar_enroll = make_clustered_bar("fact_trials", "phase", "fact_trials", "Avg Enrollment", "Average Enrollment by Phase", "Phase")
    make_visual(p3, "p3_bar_enroll", 30, 680, 1860, 360, 7000, bar_enroll)
    print("Page 3 complete.")


def build_page_4():
    p4 = os.path.join(base_dir, "page_geo_d4c3")

    # Clustered bar: Top Countries by Trial Volume
    bar_country = make_clustered_bar("dim_countries", "country", "fact_trials", "Total Trials", "Top Countries by Total Trials", "Country")
    make_visual(p4, "p4_bar_country", 30, 90, 920, 470, 1000, bar_country)

    # Clustered bar: Most Frequently Terminated Conditions
    bar_cond = make_clustered_bar("dim_conditions", "condition", "fact_trials", "Terminated Trials", "Conditions with Most Terminated Trials", "Condition")
    make_visual(p4, "p4_bar_cond", 970, 90, 920, 470, 2000, bar_cond)

    # Table / Matrix: Intervention Types and Termination
    table_interv = make_pivot_table(
        "dim_interventions", "intervention_type",
        "fact_trials", ["Total Trials", "Terminated Trials", "Termination Rate"],
        "Intervention Types & Termination Performance"
    )
    make_visual(p4, "p4_table_interv", 30, 580, 1420, 460, 3000, table_interv)

    # Slicer: Country
    make_visual(p4, "p4_slicer_country", 1470, 580, 420, 460, 4000, make_slicer("dim_countries", "country", "Filter Country"))
    print("Page 4 complete.")


if __name__ == "__main__":
    build_page_1()
    build_page_2()
    build_page_3()
    build_page_4()
    print("\nAll 4 Power BI pages built successfully!")

