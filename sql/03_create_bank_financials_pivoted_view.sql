CREATE OR REPLACE VIEW `bank-risk-bi-project.bank_risk_data.bank_financials_pivoted` AS
WITH deduped AS (
SELECT
bank_name,
cik,
field,
value,
fiscal_year,
fiscal_period,
end_date,
form,
ROW_NUMBER() OVER (
PARTITION BY bank_name, field, end_date
ORDER BY 
CASE WHEN form = '10-Q' THEN 1 
WHEN form = '10-K' THEN 2 
ELSE 3 END
) AS rn
FROM `bank-risk-bi-project.bank_risk_data.bank_financials`
WHERE form IN ('10-Q', '10-K')
)
SELECT
bank_name,
cik,
end_date,
MAX(fiscal_year) AS fiscal_year,
MAX(fiscal_period) AS fiscal_period,
MAX(IF(field = 'ProvisionForLoanLossesExpensed', value, NULL)) AS provision_expensed,
MAX(IF(field = 'ProvisionForLoanAndLeaseLosses', value, NULL)) AS provision_loan_lease,
MAX(IF(field = 'AllowanceForLoanAndLeaseLosses', value, NULL)) AS allowance_balance,
MAX(IF(field = 'NetIncomeLoss', value, NULL)) AS net_income
FROM deduped
WHERE rn = 1
GROUP BY bank_name, cik, end_date
ORDER BY bank_name, end_date