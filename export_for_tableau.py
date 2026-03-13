# ================================================
# Export cleaned data for Tableau
# ================================================

import pandas as pd
import os

os.makedirs('data/processed', exist_ok=True)

# Load raw data
orders = pd.read_csv('data/raw/Orders_and_shipments.csv',
                     encoding='latin-1', skipinitialspace=True)
inventory = pd.read_csv('data/raw/Inventory.csv',
                        encoding='latin-1', skipinitialspace=True)
fulfillment = pd.read_csv('data/raw/Fulfillment.csv',
                          encoding='latin-1', skipinitialspace=True)

# Clean column names
orders.columns = orders.columns.str.strip()
inventory.columns = inventory.columns.str.strip()
fulfillment.columns = fulfillment.columns.str.strip()

# Clean orders
orders['Discount %'] = pd.to_numeric(
    orders['Discount %'].replace(' - ', 0), errors='coerce').fillna(0)
orders['Shipment Days - Scheduled'] = orders['Shipment Days - Scheduled'].abs()
orders['Profit Margin %'] = (orders['Profit'] / orders['Gross Sales'] * 100).round(2)
orders['Order Date'] = pd.to_datetime(
    orders['Order Year'].astype(str) + '-' +
    orders['Order Month'].astype(str) + '-' +
    orders['Order Day'].astype(str)
)
orders['Delay Category'] = orders['Shipment Days - Scheduled'].apply(
    lambda x: f'{int(x)} Day Delay' if x > 0 else 'On Time'
)

# Clean inventory
inventory['Storage Cost'] = (
    inventory['Warehouse Inventory'] * inventory['Inventory Cost Per Unit']
).round(2)

# Merge for Tableau master table
master = orders.merge(inventory, on='Product Name', how='left')
master = master.merge(fulfillment, on='Product Name', how='left')

# Export
orders.to_csv('data/processed/orders_clean.csv', index=False)
inventory.to_csv('data/processed/inventory_clean.csv', index=False)
fulfillment.to_csv('data/processed/fulfillment_clean.csv', index=False)
master.to_csv('data/processed/master_tableau.csv', index=False)

print("Export complete!")
print(f"   orders_clean.csv        - {len(orders):,} rows")
print(f"   inventory_clean.csv     - {len(inventory):,} rows")
print(f"   fulfillment_clean.csv   - {len(fulfillment):,} rows")
print(f"   master_tableau.csv      - {len(master):,} rows")