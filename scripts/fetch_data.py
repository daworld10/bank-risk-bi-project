import requests
import pandas as pd
from google.cloud import bigquery
import time
import json
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\dhamin2\Box\BI Project\bank-risk-bi-project-38e9896e012c.json"

# ---- CONFIGURATION ----
FRED_API_KEY = "YOUR_FRED_API_KEY"  # Insert your FRED API key
SEC_HEADERS = {"User-Agent": "YourName your_email@example.com"}  # SEC requires this, use real contact info
BQ_PROJECT = "bank-risk-bi-project"
BQ_DATASET = "bank_risk_data"

# 16 regional banks with their SEC CIK numbers (10-digit, zero-padded)
BANKS = {
    "Zions Bancorporation": "0000109380",
    "Comerica": "0000028412",
    "M&T Bank": "0000036270",
    "Fifth Third Bancorp": "0000035527",
    "Regions Financial": "0001281761",
    "Huntington Bancshares": "0000049196",
    "KeyCorp": "0000091576",
    "Citizens Financial Group": "0000759944",
    "PNC Financial Services": "0000713676",
    "Truist Financial": "0000092230",
    "Western Alliance Bancorporation": "0001212545",
    "East West Bancorp": "0001069157",
    "Synovus Financial": "0000018349",
    "Valley National Bancorp": "0000714310",
    "Webster Financial": "0000801337",
    "Old National Bancorp": "0000707179"
}

# XBRL concept tags we want to pull for each bank
XBRL_FIELDS = [
    "ProvisionForLoanLossesExpensed",
    "ProvisionForLoanAndLeaseLosses",
    "AllowanceForLoanAndLeaseLosses",
    "NetIncomeLoss",
    "ProfitLoss"
]

# FRED series we want
FRED_SERIES = ["FEDFUNDS", "DFF", "MORTGAGE30US", "T10Y2Y"]

# ---- STEP 1: Pull SEC XBRL data for one bank ----
def get_bank_facts(cik):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    resp = requests.get(url, headers=SEC_HEADERS)
    if resp.status_code != 200:
        print(f"Failed for CIK {cik}: {resp.status_code}")
        return None
    return resp.json()

def extract_fields(bank_name, cik, facts_json):
    rows = []
    if not facts_json or "facts" not in facts_json:
        return rows
    gaap_facts = facts_json["facts"].get("us-gaap", {})
    for field in XBRL_FIELDS:
        if field in gaap_facts:
            units = gaap_facts[field]["units"].get("USD", [])
            for entry in units:
                rows.append({
                    "bank_name": bank_name,
                    "cik": cik,
                    "field": field,
                    "value": entry.get("val"),
                    "fiscal_year": entry.get("fy"),
                    "fiscal_period": entry.get("fp"),
                    "end_date": entry.get("end"),
                    "form": entry.get("form")
                })
    return rows

# ---- DEBUG: Find actual income-related tags for banks missing NetIncomeLoss ----
def debug_find_income_fields(cik, bank_name):
    facts = get_bank_facts(cik)
    if not facts or "facts" not in facts:
        print(f"No facts for {bank_name}")
        return
    gaap_facts = facts["facts"].get("us-gaap", {})
    matches = [k for k in gaap_facts.keys() if "NetIncome" in k or "ProfitLoss" in k or "Income" in k]
    print(f"{bank_name} income-related tags: {matches}")

# ---- STEP 2: Pull FRED series data ----
def get_fred_series(series_id):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json"
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    rows = []
    for obs in data.get("observations", []):
        rows.append({
            "series_id": series_id,
            "date": obs["date"],
            "value": obs["value"]
        })
    return rows

# ---- STEP 3: Load a DataFrame into BigQuery ----
def load_to_bigquery(df, table_name):
    client = bigquery.Client(project=BQ_PROJECT)
    table_id = f"{BQ_PROJECT}.{BQ_DATASET}.{table_name}"
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    print(f"Loaded {len(df)} rows into {table_id}")

# ---- MAIN EXECUTION ----
if __name__ == "__main__":
    # Pull bank financial data
    all_bank_rows = []
    for bank_name, cik in BANKS.items():
        print(f"Fetching {bank_name}...")
        facts = get_bank_facts(cik)
        rows = extract_fields(bank_name, cik, facts)
        all_bank_rows.extend(rows)
        time.sleep(0.2)  # be polite to SEC servers, avoid rate limiting

    bank_df = pd.DataFrame(all_bank_rows)
    bank_df.to_csv("bank_financials.csv", index=False)  # local backup
    load_to_bigquery(bank_df, "bank_financials")

    # Pull FRED data
    all_fred_rows = []
    for series in FRED_SERIES:
        print(f"Fetching FRED series {series}...")
        rows = get_fred_series(series)
        all_fred_rows.extend(rows)

    fred_df = pd.DataFrame(all_fred_rows)
    fred_df.to_csv("fred_rates.csv", index=False)  # local backup
    load_to_bigquery(fred_df, "fred_rates")
