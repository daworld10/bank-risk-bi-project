CREATE OR REPLACE VIEW `bank-risk-bi-project.bank_risk_data.fred_rates_pivoted` AS
SELECT
CAST(date AS DATE) AS date,
MAX(IF(series_id = 'DFF', value, NULL)) AS fed_funds_daily,
MAX(IF(series_id = 'FEDFUNDS', value, NULL)) AS fed_funds_monthly,
MAX(IF(series_id = 'MORTGAGE30US', value, NULL)) AS mortgage_30y,
MAX(IF(series_id = 'T10Y2Y', value, NULL)) AS yield_spread_10y2y
FROM `bank-risk-bi-project.bank_risk_data.fred_rates_clean`
GROUP BY date
ORDER BY date