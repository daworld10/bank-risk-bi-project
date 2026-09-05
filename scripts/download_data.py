from google.cloud import bigquery
import pandas as pd

client = bigquery.Client(project="bank-risk-bi-project")

bank_df = client.query("SELECT * FROM `bank-risk-bi-project.bank_risk_data.bank_financials`").to_dataframe()
bank_df.to_csv("bank_financials_full.csv", index=False)
print(f"Saved bank_financials_full.csv with {len(bank_df)} rows")

fred_df = client.query("SELECT * FROM `bank-risk-bi-project.bank_risk_data.fred_rates`").to_dataframe()
fred_df.to_csv("fred_rates_full.csv", index=False)
print(f"Saved fred_rates_full.csv with {len(fred_df)} rows")
