# LoanWise

**Make smarter loan decisions before they cost you lakhs.**

LoanWise is a Loan Decision Planner — not just another EMI calculator. It helps you understand the long-term impact of your loan decisions *before* you borrow, so you can compare offers, simulate prepayments, and see exactly how much interest you can save.

## Features

- **Dashboard** — At-a-glance summary of EMI, total interest, repayment, and duration.
- **EMI Calculator** — Monthly EMI, interest/principal split, completion date, and a clean doughnut chart.
- **Loan Comparison** — Side-by-side comparison of two loan offers with a clear winner.
- **What If Planner** — Simulate higher EMIs, annual prepayments, one-time prepayments, and rate reductions to see interest saved and years reduced.
- **About** — How LoanWise works and what stays private.

## Tech Stack

- Python
- Streamlit (web UI)
- pandas, numpy (calculations)
- plotly (visualizations)
- openpyxl (Excel support for future Pro export)

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
loanwise/
  app.py
  core/
    calculator.py
    comparison.py
    scenario.py
    utils.py
  ui/
    dashboard.py
    emi_page.py
    comparison_page.py
    scenario_page.py
    about_page.py
  assets/
  README.md
  requirements.txt
```

## Design Notes

- UI is fully separated from calculation logic in `core/`.
- All financial math lives in reusable, type-hinted classes — no duplication.
- The app works completely offline. No personal data is stored or transmitted.
- Structured so it can be packaged as a desktop app with minimal changes.

## Free vs Pro

The free version includes the EMI Calculator, Loan Comparison, and What If Planner. Pro placeholders (PDF/Excel export, saved scenarios, AI advisor) are shown as disabled buttons.
