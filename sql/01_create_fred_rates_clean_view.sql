CREATE OR REPLACE VIEW `bank-risk-bi-project.bank_risk_data.fred_rates_clean` AS
SELECT
series_id,
date,
SAFE_CAST(NULLIF(value, '.') AS FLOAT64) AS value
FROM `bank-risk-bi-project.bank_risk_data.fred_rates`