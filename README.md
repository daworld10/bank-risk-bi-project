# Bank Risk & Macro Analytics Dashboard

A Power BI business intelligence project analyzing credit risk and financial performance across **16 U.S. regional banks**, combining SEC regulatory filings with Federal Reserve macroeconomic data to surface early warning signals in loan provisioning behavior.

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![BigQuery](https://img.shields.io/badge/Google%20BigQuery-4285F4?style=flat&logo=googlecloud&logoColor=white)
![SEC EDGAR](https://img.shields.io/badge/Data-SEC%20EDGAR%20API-blue)
![FRED](https://img.shields.io/badge/Data-FRED%20API-red)

---

## Dashboard Preview

### Bank Risk Overview
![Bank Risk Overview](assets/screenshots/bank-risk-overview.png)

### Macro & Coverage Trends
![Macro Coverage Trends](assets/screenshots/macro-coverage-trends.png)

> **Note:** Add your exported PNG screenshots to an `assets/screenshots/` folder in this repo with the filenames above (or update the paths here to match your actual filenames) so they render on GitHub.

---

## Overview

This project tracks how loan-loss provisioning risk moves across 16 regional banks over nearly two decades (2007-2026), and connects those movements to the macroeconomic environment driving them — specifically the Fed Funds Rate and the 10-Year/2-Year Treasury yield spread.

The core question this dashboard answers: **which banks are taking on the most credit risk relative to their income, and how does that risk track with interest rate cycles?**

## Key Insights

- **Huntington Bancshares** and **Webster Financial** show the highest provision-to-income ratios across 2021-2024, with Huntington posting two extreme spikes (~-2.5 and ~-1.9) tied to specific credit events.
- **M&T Bank**, **Regions Financial**, and **Comerica** maintain the lowest, most stable provisioning ratios, indicating more conservative credit risk management.
- Provisioning risk across the sector closely tracks the Fed Funds Rate hiking cycle from 2022-2024, with banks moving from negative/near-zero provisioning to consistently positive ratios as rates climbed from ~0% to ~5.5%.
- The 10Y-2Y Treasury yield spread inverted (went negative) from mid-2022 through late 2024 — a historically reliable recession warning signal — before normalizing in 2025-2026.

## Data Sources

| Source | What It Provides | Access Method |
|---|---|---|
| **SEC EDGAR (XBRL API)** | Quarterly/annual financial statement data (Net Income, Loan Loss Provisions, Allowance for Loan Losses) for all 16 banks | `data.sec.gov/api/xbrl/companyfacts` |
| **FRED (Federal Reserve Economic Data)** | Macroeconomic time series: Fed Funds Rate, 10Y-2Y Treasury Yield Spread, 30-Year Mortgage Rate | `api.stlouisfed.org/fred/series/observations` |

**Banks covered:** Zions Bancorporation, Comerica, M&T Bank, Fifth Third Bancorp, Regions Financial, Huntington Bancshares, KeyCorp, Citizens Financial Group, PNC Financial Services, Truist Financial, Western Alliance Bancorporation, East West Bancorp, Synovus Financial, Valley National Bancorp, Webster Financial, Old National Bancorp.

## Tech Stack & Pipeline

```
SEC EDGAR API ──┐
                ├──> Python (requests, pandas) ──> Google BigQuery ──> Power BI
FRED API ───────┘
```

1. **Extraction** (`fetch_data.py`): Pulls XBRL financial facts for each bank via SEC's public API (CIK-based lookup) and macro series from FRED's API.
2. **Transformation**: Cleans and structures raw JSON responses into tabular format (bank name, fiscal period, end date, metric value), handling duplicate filings and inconsistent reporting tags across banks.
3. **Load** (`download_data.py`): Stages data into Google BigQuery tables (`bank_financials`, `fred_rates`) for centralized, queryable storage.
4. **Modeling & Visualization**: Power BI connects directly to BigQuery, with DAX measures calculating provision-to-income ratios, risk rankings (via `LASTNONBLANK`), and time-based trend aggregations.

## Dashboard Structure

The report is organized across three pages:

### 1. Bank Risk Overview
Six KPI cards (average provision-to-income ratio, current yield spread, bank count, aggregate net income, highest-risk bank, lowest-risk bank) paired with three visuals: a per-bank provisioning trend over time (2021-2024), a ranked risk comparison bar chart highlighting Huntington Bancshares as the clear outlier, and the 10-Year vs 2-Year Treasury yield spread chart with a recession-warning inversion line.

### 2. Macro & Coverage Trends
A filterable net income trend across all 16 banks (2022-2026) with an interactive bank-selector, a data reporting coverage chart validating the completeness of the underlying SEC dataset from 2007-2026, and a combo chart overlaying the Fed Funds Rate against aggregate bank provisioning risk to visualize how credit risk-taking tracked the 2022-2024 rate-hiking cycle.

### 3. Deep Dive
Detailed exploration of individual bank metrics and risk drivers for further analysis.

## Key Metrics & DAX Logic

- **Provision-to-Income Ratio**: Loan loss provisions relative to net income, the core credit-risk metric used throughout the report.
- **Highest/Lowest Risk Bank**: Calculated using `LASTNONBLANK` to identify each bank's most recent reported ratio, then ranked to surface the current highest and lowest risk institutions (Fifth Third Bancorp and Citizens Financial Group, respectively, as of the latest data refresh).
- **Yield Spread (10Y-2Y)**: A classic recession-warning indicator; a dashed red reference line at zero marks the inversion threshold.
- **Zero-line reference (bank charts)**: A solid gray constant line at y=0 separates provisioning gains from losses across the trend chart.

## Design Notes

The report uses a dark navy theme (`#1B2A41` canvas / `#1F3455` visual panels) with a green-to-red risk-tier color palette applied to bank-level visuals, so lower-risk banks (green) and higher-risk banks (red) are visually distinguishable at a glance without reading labels. All charts share consistent borders (`#3A5578`), white/light-gray text for readability against the dark background, and chart-specific reference lines (red dashed for the macro yield-curve inversion signal, gray solid for the neutral bank provisioning boundary).

## Skills Demonstrated

- API integration and data extraction (REST APIs, JSON parsing)
- Cloud data warehousing (Google BigQuery)
- Data modeling and DAX (Power BI)
- Financial statement analysis (XBRL/GAAP concepts)
- Dashboard design and data visualization best practices

## Author

Built by Dharshan Hemprakash Amin as a portfolio project demonstrating end-to-end BI development — from raw regulatory data extraction through cloud storage to an interactive analytical dashboard.
