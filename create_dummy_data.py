import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)

# Generate dummy data
num_records = 500

# Date range: April 2024 to February 2026 (spanning multiple fiscal years)
start_date = datetime(2024, 4, 1)
end_date = datetime(2026, 2, 25)
date_range = (end_date - start_date).days

# Generate random dates
dates = [start_date + timedelta(days=random.randint(0, date_range)) for _ in range(num_records)]

# Customer types
customer_types = np.random.choice(['B2B', 'B2C'], size=num_records, p=[0.4, 0.6])

# Account IDs (some repeating to simulate returning customers)
account_ids = [f"ACC{str(random.randint(1000, 1200)).zfill(5)}" for _ in range(num_records)]

# Revenue amounts (B2B typically higher than B2C)
revenue_amounts = []
for ctype in customer_types:
    if ctype == 'B2B':
        revenue_amounts.append(round(random.uniform(5000, 50000), 2))
    else:
        revenue_amounts.append(round(random.uniform(500, 5000), 2))

# Create DataFrame
df = pd.DataFrame({
    'transaction_date': dates,
    'customer_type': customer_types,
    'account_id': account_ids,
    'revenue_amount': revenue_amounts
})

# Sort by date
df = df.sort_values('transaction_date').reset_index(drop=True)

# Save to Excel
output_file = "Martech_Ashika.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"✅ Dummy data file created: {output_file}")
print(f"   Total records: {len(df)}")
print(f"\nSample data:")
print(df.head(10).to_string())
print(f"\n\nCustomer type distribution:")
print(df['customer_type'].value_counts())
