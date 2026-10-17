# Power BI Dashboard Guide — Clinical Trial Termination Analysis

## Overview

This guide walks you through building a **four-page Power BI dashboard** from the cleaned AACT data.
The dashboard mirrors (and extends) the analysis from the Jupyter notebook.

---

## Step 1 — Generate the Data Files

Run the preparation script from a terminal inside the project folder:

```powershell
cd "d:\study material\projects\clinical_trial_termination_analysis"
python prepare_powerbi_data.py
```

This creates a `powerbi_data/` folder containing:

| File | Description | Grain |
|---|---|---|
| `fact_trials.csv` | One row per trial — statuses, phase, sponsor, reason, dates | nct_id |
| `dim_conditions.csv` | Disease/condition names linked to trials | nct_id × condition |
| `dim_countries.csv` | Country of each trial site | nct_id × country |
| `dim_sponsors.csv` | Sponsor names and classes | nct_id × sponsor |
| `dim_interventions.csv` | Intervention types and names | nct_id × intervention |

---

## Step 2 — Import into Power BI

1. Open **Power BI Desktop**.
2. Click **Home → Get Data → Text/CSV**.
3. Load each of the five CSV files from `powerbi_data/`.
4. In **Transform Data** (Power Query Editor):
   - Verify column types (especially that `start_year`, `enrollment` are **Whole Number**, and `terminated` is **Whole Number** 0/1).
   - Close & Apply.

---

## Step 3 — Set Up the Data Model (Relationships)

Go to **Model view** and create these relationships (all **Many-to-One**, single direction):

```
dim_conditions[nct_id]     →  fact_trials[nct_id]   (many-to-one)
dim_countries[nct_id]      →  fact_trials[nct_id]    (many-to-one)
dim_sponsors[nct_id]       →  fact_trials[nct_id]    (many-to-one)
dim_interventions[nct_id]  →  fact_trials[nct_id]    (many-to-one)
```

> [!IMPORTANT]
> Cross-filter direction should be **Single** (from dimension to fact) to avoid ambiguity.

---

## Step 4 — Create DAX Measures

Add these measures to the `fact_trials` table:

```dax
// Core counts
Total Trials = COUNTROWS(fact_trials)

Terminated Trials = CALCULATE(COUNTROWS(fact_trials), fact_trials[terminated] = 1)

Completed Trials = CALCULATE(COUNTROWS(fact_trials), fact_trials[terminated] = 0)

Termination Rate = DIVIDE([Terminated Trials], [Total Trials], 0)

// Per-100 rate (for the bar charts)
Terminated per 100 = [Termination Rate] * 100

// Average enrollment
Avg Enrollment = AVERAGE(fact_trials[enrollment])
```

---

## Step 5 — Build the Dashboard Pages

### Page 1: Executive Overview

| Visual | Fields | Notes |
|---|---|---|
| **Card** | `[Total Trials]` | Big number, top left |
| **Card** | `[Terminated Trials]` | Top center |
| **Card** | `[Termination Rate]` | Format as %, top right |
| **Donut chart** | Legend = `overall_status`, Values = `[Total Trials]` | Completed vs Terminated split |
| **Stacked bar** | Axis = `phase`, Values = `[Total Trials]`, Legend = `overall_status` | Shows which phases have more terminations |
| **Line chart** | X-axis = `start_year`, Values = `[Termination Rate]` | Trend over time |
| **Slicer** | `start_year` (range slider) | Filter all visuals |
| **Slicer** | `phase` (dropdown or list) | Filter all visuals |

#### Colour scheme suggestion
- Completed: `#5B9BD5` (blue)
- Terminated: `#ED7D31` (orange)

---

### Page 2: Termination Reasons

| Visual | Fields | Notes |
|---|---|---|
| **Stacked bar** (horizontal) | Axis = `termination_reason`, Values = `[Terminated Trials]` | Sort descending; exclude "Completed" |
| **100% stacked bar** | Axis = `phase`, Values = `[Terminated Trials]`, Legend = `termination_reason` | Reason mix by phase |
| **Clustered bar** | Axis = `termination_reason`, Values = `[Terminated per 100]`, Legend = `sponsor_group` | Recreates the notebook's key chart |
| **Table / Matrix** | Rows = `termination_reason`, Columns = `sponsor_group`, Values = `[Terminated Trials]` | Cross-tab detail |
| **Slicer** | `phase` | |
| **Slicer** | `sponsor_group` | |

> [!TIP]
> For the clustered bar, filter the visual to show only `INDUSTRY` and `OTHER` sponsor groups and only `PHASE2` + `PHASE3` to match Section 9 of the notebook.

---

### Page 3: Sponsor & Phase Deep-Dive

| Visual | Fields | Notes |
|---|---|---|
| **Matrix** | Rows = `sponsor_group`, Columns = `phase`, Values = `[Total Trials]`, `[Termination Rate]` | Conditional formatting on termination rate (green → red) |
| **Clustered column** | X = `source_class`, Values = `[Termination Rate]` | Raw rate by detailed sponsor class |
| **Scatter plot** | X = `[Avg Enrollment]`, Y = `[Termination Rate]`, Legend = `phase` | Explore enrollment vs termination |
| **Card** | `[Terminated Trials]` filtered to `sponsor_group = INDUSTRY` | Quick industry count |
| **Card** | `[Terminated Trials]` filtered to `sponsor_group = OTHER` | Quick other count |

---

### Page 4: Geography & Conditions

| Visual | Fields | Notes |
|---|---|---|
| **Map** (filled or bubble) | Location = `dim_countries[country]`, Size = `[Total Trials]`, Colour = `[Termination Rate]` | Global trial distribution |
| **Treemap** | Group = `dim_conditions[condition]`, Values = `[Terminated Trials]` | Most terminated conditions |
| **Top N bar** | `dim_conditions[condition]` by `[Termination Rate]`, Top 20 | Conditions with highest termination rate |
| **Table** | `dim_interventions[intervention_type]`, `[Total Trials]`, `[Termination Rate]` | Breakdown by intervention type |

> [!NOTE]
> The conditions and countries tables have a many-to-many grain against trials (a trial can list multiple conditions/countries). Power BI's bidirectional filtering handles this, but check your totals against the notebook's 289,595 to make sure counts aren't inflated.

---

## Step 6 — Formatting & Polish

1. **Theme**: Apply a professional theme — try *Executive*, *Innovate*, or a custom JSON theme.
2. **Title bar**: Add a text box at the top of each page: *"Clinical Trial Termination Analysis — ClinicalTrials.gov (AACT)"*.
3. **Conditional formatting**: On matrices and tables, use background colour scales (green-to-red) on `[Termination Rate]`.
4. **Tooltips**: Add `brief_title` and `why_stopped` as tooltip fields so hovering shows the raw reason text.
5. **Bookmarks**: Create bookmarks for "Phase 2 focus" and "Phase 3 focus" with pre-set slicer states.
6. **Source note**: Add a footer text: *"Source: ClinicalTrials.gov via AACT. Reasons classified by keyword rules."*

---

## Data Model Diagram

```
┌───────────────────┐
│  dim_conditions   │
│  nct_id, condition│───┐
└───────────────────┘   │
                        │   ┌─────────────────────────────────────┐
┌───────────────────┐   ├──►│            fact_trials               │
│  dim_countries    │   │   │  nct_id (PK)                        │
│  nct_id, country  │───┤   │  phase, sponsor_group, terminated   │
└───────────────────┘   │   │  termination_reason, enrollment     │
                        │   │  start_year, completion_year        │
┌───────────────────┐   │   │  ...                                │
│  dim_sponsors     │───┤   └─────────────────────────────────────┘
│  nct_id, sponsor  │   │
└───────────────────┘   │
                        │
┌───────────────────┐   │
│ dim_interventions │───┘
│  nct_id, type     │
└───────────────────┘
```

---

## Quick Reference — Key Findings to Highlight

These callout numbers from the notebook make great dashboard text boxes:

- **10.3%** of finished interventional trials were terminated
- **Phase 1/2** has the highest termination odds (OR 1.85 vs Phase 3)
- **Industry vs OTHER** — OR 1.02 after adjustment (not significantly different)
- **Enrollment** is the #1 stated reason for termination
- **Pseudo R² = 0.03** — the model is descriptive, not predictive

