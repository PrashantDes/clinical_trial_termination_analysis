"""
Prepare Power BI-ready CSV files from the AACT clinical trial data.

Applies the same filters and reason-classification logic used in
clinical_trial_termination_analysis.ipynb, then exports a star-schema
set of tables optimised for Power BI:

  powerbi_data/
    fact_trials.csv          – one row per trial (the fact table)
    dim_conditions.csv       – condition names keyed by nct_id
    dim_countries.csv        – countries keyed by nct_id
    dim_sponsors.csv         – sponsor names & classes keyed by nct_id
    dim_interventions.csv    – intervention types & names keyed by nct_id

Usage
-----
    pip install pandas numpy
    python prepare_powerbi_data.py

The script reads from the `data/` subfolder (or the AACT_DIR environment
variable) and writes into `powerbi_data/`.
"""

import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 0.  Configuration
# ---------------------------------------------------------------------------
DATA_DIR = Path(os.environ.get("AACT_DIR", "data"))
OUT_DIR = Path("powerbi_data")
OUT_DIR.mkdir(exist_ok=True)

print("Reading AACT data …")

# ---------------------------------------------------------------------------
# 1.  Load the studies table
# ---------------------------------------------------------------------------
studies = pd.read_csv(DATA_DIR / "studies.txt", sep="|", low_memory=False)
print(f"  studies.txt loaded: {len(studies):,} rows")

# ---------------------------------------------------------------------------
# 2.  Filter to interventional, finished trials
# ---------------------------------------------------------------------------
df = studies[
    (studies["study_type"] == "INTERVENTIONAL")
    & (studies["overall_status"].isin(["COMPLETED", "TERMINATED"]))
].copy()

df["terminated"] = (df["overall_status"] == "TERMINATED").astype(int)
df["phase"] = df["phase"].fillna("NA")
print(f"  Interventional & finished: {len(df):,} rows")

# ---------------------------------------------------------------------------
# 3.  Parse dates and extract year
# ---------------------------------------------------------------------------
df["start_date_parsed"] = pd.to_datetime(df["start_date"], errors="coerce")
df["start_year"] = df["start_date_parsed"].dt.year.astype("Int64")
df["start_month"] = df["start_date_parsed"].dt.to_period("M").astype(str)

df["completion_date_parsed"] = pd.to_datetime(df["completion_date"], errors="coerce")
df["completion_year"] = df["completion_date_parsed"].dt.year.astype("Int64")

# ---------------------------------------------------------------------------
# 4.  Classify the free-text stop reasons (same rules as notebook)
# ---------------------------------------------------------------------------
rules = [
    ("COVID-19",            r"covid|pandemic"),
    ("Safety",              r"safety|toxic|adverse|death|mortality|reactogenicity"
                            r"|halting criteria|side effect|\bharm"),
    ("Enrollment",          r"accrual|enroll|recruit|inclusion|low number|too few"
                            r"|poor participation"
                            r"|insufficient (number|patient|subject|participant)"),
    ("Efficacy/futility",   r"futil|efficacy|insufficient (effect|activity|benefit)"
                            r"|no (significant )?(difference|effect|benefit)"
                            r"|did not (meet|demonstrate|show)|ineffective"
                            r"|lack of (effect|benefit)"
                            r"|primary (outcome|endpoint)|interim|preliminary results"),
    ("Drug supply",         r"supply|unavailable|no longer available|recall|shelf"
                            r"|manufactur|expired"),
    ("Regulatory",          r"\bfda\b|\bema\b|regulatory|ethic|\birb\b|approval"),
    ("Funding",             r"\bfund(s|ed|ing)?\b|financ|budget|cost|\bgrant"),
    ("Sponsor/business",    r"sponsor|business|strategic|compan|portfolio"
                            r"|commercial|priorit"),
    ("Design/feasibility",  r"\bdesign|protocol|amend|modif|sample size|feasib"
                            r"|methodolog|supersed"),
    ("Staff/investigator",  r"investigator|\bpi\b|cancel|relocat|left the|retire"
                            r"|\bmoved|surgeon|staff|personnel|\bresident"),
]


def categorize(reason: str) -> str:
    """Return the first matching category for a free-text stop reason."""
    r = str(reason).lower().strip()
    if r in ("", "nan") or "see termination reason" in r:
        return "Not given"
    for name, pattern in rules:
        if re.search(pattern, r):
            return name
    return "Other"


df["termination_reason"] = df["why_stopped"].apply(categorize)
# Mark completed trials explicitly
df.loc[df["terminated"] == 0, "termination_reason"] = "Completed"

# ---------------------------------------------------------------------------
# 5.  Clean up sponsor grouping (same as notebook Section 10)
# ---------------------------------------------------------------------------
df["sponsor_group"] = df["source_class"].where(
    df["source_class"].isin(
        ["INDUSTRY", "OTHER", "NIH", "FED", "NETWORK", "OTHER_GOV"]
    ),
    "OTHER",
)

# ---------------------------------------------------------------------------
# 6.  Build the Fact table
# ---------------------------------------------------------------------------
fact_cols = [
    "nct_id",
    "brief_title",
    "overall_status",
    "terminated",
    "phase",
    "enrollment",
    "enrollment_type",
    "source",
    "source_class",
    "sponsor_group",
    "number_of_arms",
    "number_of_groups",
    "why_stopped",
    "termination_reason",
    "has_dmc",
    "is_fda_regulated_drug",
    "is_fda_regulated_device",
    "start_year",
    "start_month",
    "completion_year",
]

fact = df[fact_cols].copy()
fact.to_csv(OUT_DIR / "fact_trials.csv", index=False, encoding="utf-8-sig")
print(f"  fact_trials.csv written: {len(fact):,} rows")

# ---------------------------------------------------------------------------
# 7.  Dimension: conditions
# ---------------------------------------------------------------------------
conditions = pd.read_csv(DATA_DIR / "conditions.txt", sep="|", low_memory=False)
dim_cond = conditions[conditions["nct_id"].isin(df["nct_id"])][
    ["nct_id", "name"]
].copy()
dim_cond.rename(columns={"name": "condition"}, inplace=True)
dim_cond.to_csv(OUT_DIR / "dim_conditions.csv", index=False, encoding="utf-8-sig")
print(f"  dim_conditions.csv written: {len(dim_cond):,} rows")

# ---------------------------------------------------------------------------
# 8.  Dimension: countries
# ---------------------------------------------------------------------------
countries = pd.read_csv(DATA_DIR / "countries.txt", sep="|", low_memory=False)
dim_country = countries[
    (countries["nct_id"].isin(df["nct_id"])) & (countries["removed"] != "t")
][["nct_id", "name"]].copy()
dim_country.rename(columns={"name": "country"}, inplace=True)
dim_country.to_csv(OUT_DIR / "dim_countries.csv", index=False, encoding="utf-8-sig")
print(f"  dim_countries.csv written: {len(dim_country):,} rows")

# ---------------------------------------------------------------------------
# 9.  Dimension: sponsors
# ---------------------------------------------------------------------------
sponsors = pd.read_csv(DATA_DIR / "sponsors.txt", sep="|", low_memory=False)
dim_sponsor = sponsors[sponsors["nct_id"].isin(df["nct_id"])][
    ["nct_id", "agency_class", "lead_or_collaborator", "name"]
].copy()
dim_sponsor.rename(
    columns={"name": "sponsor_name", "agency_class": "sponsor_class"},
    inplace=True,
)
dim_sponsor.to_csv(OUT_DIR / "dim_sponsors.csv", index=False, encoding="utf-8-sig")
print(f"  dim_sponsors.csv written: {len(dim_sponsor):,} rows")

# ---------------------------------------------------------------------------
# 10. Dimension: interventions
# ---------------------------------------------------------------------------
interventions = pd.read_csv(DATA_DIR / "interventions.txt", sep="|", low_memory=False)
dim_interv = interventions[interventions["nct_id"].isin(df["nct_id"])][
    ["nct_id", "intervention_type", "name"]
].copy()
dim_interv.rename(columns={"name": "intervention_name"}, inplace=True)
dim_interv.to_csv(OUT_DIR / "dim_interventions.csv", index=False, encoding="utf-8-sig")
print(f"  dim_interventions.csv written: {len(dim_interv):,} rows")

# ---------------------------------------------------------------------------
# 11. Summary
# ---------------------------------------------------------------------------
print("\n[OK] All files written to:", OUT_DIR.resolve())
print("\nTable summary:")
print(f"  fact_trials        {len(fact):>10,} rows")
print(f"  dim_conditions     {len(dim_cond):>10,} rows")
print(f"  dim_countries      {len(dim_country):>10,} rows")
print(f"  dim_sponsors       {len(dim_sponsor):>10,} rows")
print(f"  dim_interventions  {len(dim_interv):>10,} rows")
print("\nOpen Power BI Desktop → Get Data → Text/CSV → load these files.")
print("See powerbi_guide.md for step-by-step dashboard instructions.")
