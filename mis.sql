-- Create Table
CREATE TABLE transactions (
    transaction_date DATE,
    account_id INT,
    customer_type VARCHAR(10),   -- B2C / B2B / RA
    revenue_amount DECIMAL(12,2)
);


-- Insert Data
INSERT INTO transactions (transaction_date, account_id, customer_type, revenue_amount) VALUES
('2024-04-01', 1001, 'B2C', 1000.00),
('2024-04-02', 1002, 'B2B', 2000.00),
('2024-04-03', 1003, 'RA', 3000.00),
('2024-04-04', 1004, 'B2C', 4000.00),
('2024-04-05', 1005, 'B2B', 5000.00),
('2024-04-06', 1006, 'RA', 6000.00);


-- 1. Create a base_data CTE with enriched columns
WITH base_data AS (

    SELECT
        transaction_date,
        account_id,
        customer_type,
        revenue_amount,

        -- Month in 'Mon-YY' format (e.g. Apr-24)
        DATE_FORMAT(transaction_date, '%b-%y') AS month,

        -- Fiscal Year as per India (Apr–Mar)
        CASE
            WHEN MONTH(transaction_date) >= 4 THEN
                CONCAT(
                    'FY ',
                    RIGHT(YEAR(transaction_date),2),'-',
                    RIGHT(YEAR(transaction_date)+1,2)
                )
            ELSE
                CONCAT(
                    'FY ',
                    RIGHT(YEAR(transaction_date)-1,2),'-',
                    RIGHT(YEAR(transaction_date),2)
                )
        END AS fiscal_year

    FROM transactions
)

-- 1. Month-wise Account MIS    
SELECT
    month,

    COUNT(DISTINCT CASE WHEN customer_type='B2C' THEN account_id END) AS B2C,
    COUNT(DISTINCT CASE WHEN customer_type='B2B' THEN account_id END) AS B2B,
    COUNT(DISTINCT CASE WHEN customer_type='RA' THEN account_id END)  AS RA,

    COUNT(DISTINCT account_id) AS Total,

    ROUND(
        COUNT(DISTINCT CASE WHEN customer_type='B2C' THEN account_id END)*100.0 /
        COUNT(DISTINCT account_id)
    , 2) AS B2C_percentage,

    ROUND(
        COUNT(DISTINCT CASE WHEN customer_type='B2B' THEN account_id END)*100.0 /
        COUNT(DISTINCT account_id)
    , 2) AS B2B_percentage,

    ROUND(
        COUNT(DISTINCT CASE WHEN customer_type='RA' THEN account_id END)*100.0 /
        COUNT(DISTINCT account_id)
    , 2) AS RA_percentage

FROM base_data
GROUP BY month
ORDER BY STR_TO_DATE(month,'%b-%y');


-- 2. Month-wise Revenue MIS
SELECT
    month,

    SUM(CASE WHEN customer_type='B2C' THEN revenue_amount ELSE 0 END) AS B2C,
    SUM(CASE WHEN customer_type='B2B' THEN revenue_amount ELSE 0 END) AS B2B,
    SUM(CASE WHEN customer_type='RA' THEN revenue_amount ELSE 0 END)  AS RA,

    SUM(revenue_amount) AS Total,

    ROUND(
        SUM(CASE WHEN customer_type='B2C' THEN revenue_amount ELSE 0 END)*100.0 /
        SUM(revenue_amount)
    , 2) AS B2C_percentage,

    ROUND(
        SUM(CASE WHEN customer_type='B2B' THEN revenue_amount ELSE 0 END)*100.0 /
        SUM(revenue_amount)
    , 2) AS B2B_percentage,

    ROUND(
        SUM(CASE WHEN customer_type='RA' THEN revenue_amount ELSE 0 END)*100.0 /
        SUM(revenue_amount)
    , 2) AS RA_percentage

FROM base_data
GROUP BY month
ORDER BY STR_TO_DATE(month,'%b-%y');


-- 3. Fiscal Year Accounts MIS
SELECT
    fiscal_year,

    COUNT(DISTINCT CASE WHEN customer_type='B2C' THEN account_id END) AS B2C,
    COUNT(DISTINCT CASE WHEN customer_type='B2B' THEN account_id END) AS B2B,
    COUNT(DISTINCT CASE WHEN customer_type='RA' THEN account_id END)  AS RA,

    COUNT(DISTINCT account_id) AS Total,

    ROUND(
        COUNT(DISTINCT CASE WHEN customer_type='B2C' THEN account_id END)*100.0 /
        COUNT(DISTINCT account_id)
    , 2) AS B2C_percentage,

    ROUND(
        COUNT(DISTINCT CASE WHEN customer_type='B2B' THEN account_id END)*100.0 /
        COUNT(DISTINCT account_id)
    , 2) AS B2B_percentage,

    ROUND(
        COUNT(DISTINCT CASE WHEN customer_type='RA' THEN account_id END)*100.0 /
        COUNT(DISTINCT account_id)
    , 2) AS RA_percentage

FROM base_data
GROUP BY fiscal_year
ORDER BY fiscal_year;


-- 4. Fiscal Year Revenue MIS
SELECT
    fiscal_year,

    SUM(CASE WHEN customer_type='B2C' THEN revenue_amount ELSE 0 END) AS B2C,
    SUM(CASE WHEN customer_type='B2B' THEN revenue_amount ELSE 0 END) AS B2B,
    SUM(CASE WHEN customer_type='RA' THEN revenue_amount ELSE 0 END)  AS RA,

    SUM(revenue_amount) AS Total,

    ROUND(
        SUM(CASE WHEN customer_type='B2C' THEN revenue_amount ELSE 0 END)*100.0 /
        SUM(revenue_amount)
    , 2) AS B2C_percentage,

    ROUND(
        SUM(CASE WHEN customer_type='B2B' THEN revenue_amount ELSE 0 END)*100.0 /
        SUM(revenue_amount)
    , 2) AS B2B_percentage,

    ROUND(
        SUM(CASE WHEN customer_type='RA' THEN revenue_amount ELSE 0 END)*100.0 /
        SUM(revenue_amount)
    , 2) AS RA_percentage

FROM base_data
GROUP BY fiscal_year
ORDER BY fiscal_year;


