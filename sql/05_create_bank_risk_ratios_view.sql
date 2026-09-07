CREATE OR REPLACE VIEW `bank-risk-bi-project.bank_risk_data.bank_risk_ratios` AS
SELECT
*,
SAFE_DIVIDE(provision_loan_lease, net_income) AS provision_to_income_ratio,
SAFE_DIVIDE(allowance_balance, provision_loan_lease) AS allowance_to_provision_ratio
FROM `bank-risk-bi-project.bank_risk_data.bank_risk_master`
ORDER BY bank_name, end_date