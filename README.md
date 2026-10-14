# Why Do Clinical Trials Stop Early?

Analysis of 289,595 finished interventional trials from [ClinicalTrials.gov](https://clinicaltrials.gov), using the AACT database.

**Question:** Why do some clinical trials stop early, and does it depend on trial phase or on who sponsors the trial?

## What I did
1. Loaded the AACT `studies` table (606,820 registered studies) and kept finished interventional trials (completed or terminated).
2. Cleaned the free-text `why_stopped` column by sorting reasons into categories with keyword rules, then checked samples by eye.
3. Compared stop reasons by phase and by sponsor type, first as shares of terminated trials, then as rates per 100 finished trials.
4. Fitted a logistic regression to see which factors matter when considered together.

## Key results
- About 10% of finished trials were terminated.
- Phase 1/2 (OR 1.85) and Phase 2 (OR 1.52) trials have the highest odds of early termination versus Phase 3. Non-drug trials have the lowest (OR 0.51).
- Industry sponsorship is not associated with termination once phase is controlled (OR 1.02, 95% CI 0.99 to 1.05). The higher raw industry rate comes from its mix of phases.
- The stated reasons differ by sponsor type: industry leans toward business and safety reasons, academic and other sponsors toward enrollment and funding.
- The model explains little (pseudo R² = 0.03), so the findings are descriptive, not predictive.

## Limitations
Stated reasons are not proven causes. Keyword rules make mistakes and give one label per trial. The data are observational, and disease area and trial size are not controlled for. Full details are in the notebook.

## How to run
1. Download the monthly pipe-delimited flat files from the [AACT download page](https://aact.ctti-clinicaltrials.org/downloads) and unzip them.
2. Place them in `data/aact/` (so `data/aact/studies.txt` exists), or set the `AACT_DIR` environment variable.
3. `pip install -r requirements.txt`
4. Open `clinical_trial_termination_analysis.ipynb` and choose **Kernel > Restart & Run All**.

## Files
- `clinical_trial_termination_analysis.ipynb`: the full analysis
- `images/`: charts produced by the notebook
- `requirements.txt`: Python packages

Data: ClinicalTrials.gov via AACT (CTTI). Use is subject to the ClinicalTrials.gov terms and conditions.
