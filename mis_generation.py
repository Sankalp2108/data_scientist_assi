import pandas as pd

# 1. LOAD DATA
INPUT_FILE = "Martech_Ashika.xlsx"

df = pd.read_excel(INPUT_FILE)

# 2. DATA PREPARATION
# Convert date column
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# Create Month column (Apr-25 format)
df['Month'] = df['transaction_date'].dt.strftime('%b-%y')


# -------- Fiscal Year Function (India: Apr–Mar) ----------
def get_fiscal_year(date):
    if date.month >= 4:
        return f"FY {str(date.year)[-2:]}-{str(date.year+1)[-2:]}"
    else:
        return f"FY {str(date.year-1)[-2:]}-{str(date.year)[-2:]}"


df['Fiscal_Year'] = df['transaction_date'].apply(get_fiscal_year)


# 3. MONTH-WISE ACCOUNTS MIS
monthly_accounts = (
    df.groupby(['Month', 'customer_type'])['account_id']
      .nunique()
      .reset_index(name='accounts')
)

monthly_accounts_pivot = monthly_accounts.pivot(
    index='Month',
    columns='customer_type',
    values='accounts'
).fillna(0)

monthly_accounts_pivot['Total'] = monthly_accounts_pivot.sum(axis=1)

monthly_accounts_pivot['B2C %'] = (
    monthly_accounts_pivot.get('B2C', 0)
    / monthly_accounts_pivot['Total'] * 100
).round(2)

monthly_accounts_pivot['B2B %'] = (
    monthly_accounts_pivot.get('B2B', 0)
    / monthly_accounts_pivot['Total'] * 100
).round(2)


# 4. MONTH-WISE REVENUE MIS
monthly_revenue = (
    df.groupby(['Month', 'customer_type'])['revenue_amount']
      .sum()
      .reset_index()
)

monthly_revenue_pivot = monthly_revenue.pivot(
    index='Month',
    columns='customer_type',
    values='revenue_amount'
).fillna(0)

monthly_revenue_pivot['Total'] = monthly_revenue_pivot.sum(axis=1)

monthly_revenue_pivot['B2C %'] = (
    monthly_revenue_pivot.get('B2C', 0)
    / monthly_revenue_pivot['Total'] * 100
).round(2)

monthly_revenue_pivot['B2B %'] = (
    monthly_revenue_pivot.get('B2B', 0)
    / monthly_revenue_pivot['Total'] * 100
).round(2)


# 5. FISCAL YEAR ACCOUNTS MIS
fy_accounts = (
    df.groupby(['Fiscal_Year', 'customer_type'])['account_id']
      .nunique()
      .reset_index(name='accounts')
)

fy_accounts_pivot = fy_accounts.pivot(
    index='Fiscal_Year',
    columns='customer_type',
    values='accounts'
).fillna(0)

fy_accounts_pivot['Total'] = fy_accounts_pivot.sum(axis=1)

fy_accounts_pivot['B2C %'] = (
    fy_accounts_pivot.get('B2C', 0)
    / fy_accounts_pivot['Total'] * 100
).round(2)

fy_accounts_pivot['B2B %'] = (
    fy_accounts_pivot.get('B2B', 0)
    / fy_accounts_pivot['Total'] * 100
).round(2)

# 6. FISCAL YEAR REVENUE MIS
fy_revenue = (
    df.groupby(['Fiscal_Year', 'customer_type'])['revenue_amount']
      .sum()
      .reset_index()
)

fy_revenue_pivot = fy_revenue.pivot(
    index='Fiscal_Year',
    columns='customer_type',
    values='revenue_amount'
).fillna(0)

fy_revenue_pivot['Total'] = fy_revenue_pivot.sum(axis=1)

fy_revenue_pivot['B2C %'] = (
    fy_revenue_pivot.get('B2C', 0)
    / fy_revenue_pivot['Total'] * 100
).round(2)

fy_revenue_pivot['B2B %'] = (
    fy_revenue_pivot.get('B2B', 0)
    / fy_revenue_pivot['Total'] * 100
).round(2)

# 7. EXPORT FINAL MIS REPORT
OUTPUT_FILE = "MIS_Output.xlsx"

with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
    monthly_accounts_pivot.to_excel(writer, sheet_name="Monthly_Accounts")
    monthly_revenue_pivot.to_excel(writer, sheet_name="Monthly_Revenue")
    fy_accounts_pivot.to_excel(writer, sheet_name="FY_Accounts")
    fy_revenue_pivot.to_excel(writer, sheet_name="FY_Revenue")

print("MIS Report Generated Successfully!")
print(f"Output File: {OUTPUT_FILE}")