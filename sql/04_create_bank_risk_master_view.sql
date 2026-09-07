CREATE OR REPLACE VIEW `bank-risk-bi-project.bank_risk_data.bank_risk_master` AS
SELECT
b.bank_name,
b.cik,
b.end_date,
b.fiscal_year,
b.fiscal_period,
b.provision_expensed,
b.provision_loan_lease,
b.allowance_balance,
b.net_income,
r.avg_fed_funds_daily,
r.avg_fed_funds_monthly,
r.avg_mortgage_30y,
r.avg_yield_spread_10y2y
FROM `bank-risk-bi-project.bank_risk_data.bank_financials_pivoted` b
LEFT JOIN `bank-risk-bi-project.bank_risk_data.fred_rates_quarterly` r
ON CAST(b.end_date AS DATE) = r.quarter_end
ORDER BY b.bank_name, b.end_date