# Bank Risk BI Project

An end-to-end Business Intelligence and data engineering project analyzing **regional bank financial risk indicators** against **Federal Reserve interest rate data**. Built to demonstrate a full pipeline: raw data ingestion, cloud data warehousing, SQL transformation, and interactive dashboarding.

## Overview

This project investigates how rising/falling interest rates correlate with financial stress signals (provisioning behavior, net income volatility, yield curve dynamics) across 16 regional banks, using public regulatory and macroeconomic data spanning 2007-2026.

## Tech Stack

- **Data Sources:** SEC EDGAR (bank filings), FRED (Federal Reserve Economic Data)
- **Data Warehouse:** Google BigQuery
- **Transformation:** SQL
- **Visualization:** Power BI
- **Pipeline Scripts:** Python (`scripts/fetch_data.py`, `scripts/download_data.py`)

## Architecture

1. **Ingestion** — Python scripts pull filings data from SEC EDGAR and interest rate series from FRED via their public APIs.
2. **Storage** — Raw and cleaned data is loaded into BigQuery tables.
3. **Transformation** — SQL views model risk indicators by bank and by reporting period, joined against Fed rate movements.
4. **Visualization** — Power BI connects to the modeled data to produce an interactive dashboard tracking risk indicators by bank and end date.

## SQL Data Pipeline

All transformation logic lives in BigQuery as chained SQL views (see [`sql/`](./sql)), applied in this order:

1. **[`fred_rates_clean`](sql/01_create_fred_rates_clean_view.sql)** — casts raw FRED values to `FLOAT64`, safely handling FRED's `.` placeholder for missing observations.
2. **[`fred_rates_pivoted`](sql/02_create_fred_rates_pivoted_view.sql)** — pivots long-format FRED series (Fed Funds daily/monthly, 30-year mortgage rate, 10Y-2Y yield spread) into one row per date.
3. **[`bank_financials_pivoted`](sql/03_create_bank_financials_pivoted_view.sql)** — deduplicates overlapping 10-Q/10-K filings per bank and period (preferring 10-Q), then pivots key XBRL fields (provisions, allowances, net income) into one row per bank per `end_date`.
4. **[`bank_risk_master`](sql/04_create_bank_risk_master_view.sql)** — joins pivoted bank financials to quarterly-aggregated FRED rates on fiscal quarter end date.
5. **[`bank_risk_ratios`](sql/05_create_bank_risk_ratios_view.sql)** — computes the core risk metrics used throughout the dashboard: `provision_to_income_ratio` and `allowance_to_provision_ratio`, using `SAFE_DIVIDE` to avoid divide-by-zero errors.

This final `bank_risk_ratios` view is the direct data source for the Power BI report.

## Dashboard Preview

### Bank Risk Overview
KPI summary (avg provision ratio, current yield spread, highest/lowest risk banks, bank count), provision-to-income trend by bank, and provision-to-income ranking.

![Bank Risk Overview](screenshots/bank_risk_overview.png)

### Macro & Coverage Trends
Net income trends by bank, historical bank reporting coverage (2007-2026), and Fed Funds Rate plotted against aggregate provisioning risk.

![Macro & Coverage Trends](screenshots/macro_coverage_trends.png)

<details>
<summary>Individual chart views</summary>

**KPI Summary Cards**
![KPI Summary Cards](screenshots/kpi_summary_cards.png)

**Provision-to-Income Ratio Trend by Bank**
![Provision to Income Trend](screenshots/provision_to_income_trend.png)

**10-Year vs 2-Year Treasury Yield Spread (2007-2025)**
![Yield Spread](screenshots/yield_spread_10y_2y.png)

**Provision-to-Income Ratio by Bank (2021-2024 Average)**
![Provision to Income by Bank](screenshots/provision_to_income_by_bank.png)

**Sum of Net Income by End Date and Bank Name**
![Net Income Trend](screenshots/net_income_trend.png)

**Bank Reporting Coverage by Year (2007-2026)**
![Bank Reporting Coverage](screenshots/bank_reporting_coverage.png)

**Fed Funds Rate vs. Bank Provisioning Risk (2021-2026)**
![Fed Funds vs Provisioning Risk](screenshots/fed_funds_vs_provisioning_risk.png)

</details>

The full interactive report is available as a downloadable Power BI file: [`bank_risk_dashboard.pbix`](./bank_risk_dashboard.pbix). Open it in [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free) to explore all pages, filters, and tooltips.

## Repository Structure

```
.
├── README.md
├── bank_risk_dashboard.pbix   # Full interactive Power BI report
├── screenshots/               # Dashboard preview images
├── sql/                       # BigQuery view definitions (transformation pipeline)
│   ├── 01_create_fred_rates_clean_view.sql
│   ├── 02_create_fred_rates_pivoted_view.sql
│   ├── 03_create_bank_financials_pivoted_view.sql
│   ├── 04_create_bank_risk_master_view.sql
│   └── 05_create_bank_risk_ratios_view.sql
└── scripts/
    ├── fetch_data.py          # Pulls data from SEC EDGAR + FRED APIs
    └── download_data.py       # Handles local data download/staging
```

## Getting Started

1. Clone this repository.
2. Review `scripts/fetch_data.py` to see how source data is pulled from SEC EDGAR and FRED.
3. Review the `sql/` folder to see how raw data is transformed into risk metrics in BigQuery.
4. Open `bank_risk_dashboard.pbix` in Power BI Desktop to explore the finished dashboard.

## Key Skills Demonstrated

- API-based data ingestion (SEC EDGAR, FRED)
- Cloud data warehousing with BigQuery
- SQL-based data modeling and transformation (window functions, pivoting, safe joins/division)
- Interactive BI dashboard design in Power BI
- End-to-end project structuring for reproducibility

## Author

Built by [daworld10](https://github.com/daworld10) as a portfolio project demonstrating BI engineering skills across the full data pipeline, from raw ingestion to business-facing visualization.
