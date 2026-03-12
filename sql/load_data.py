import duckdb
import pandas as pd

conn = duckdb.connect('sql/supply_chain.db')

orders = pd.read_csv('data/raw/Orders_and_shipments.csv', skipinitialspace=True, encoding='latin-1')
inventory = pd.read_csv('data/raw/Inventory.csv', skipinitialspace=True, encoding='latin-1')
fulfillment = pd.read_csv('data/raw/Fulfillment.csv', skipinitialspace=True, encoding='latin-1')

# Strip whitespace from column names
orders.columns = orders.columns.str.strip()
inventory.columns = inventory.columns.str.strip()
fulfillment.columns = fulfillment.columns.str.strip()

conn.execute("CREATE OR REPLACE TABLE orders AS SELECT * FROM orders")
conn.execute("CREATE OR REPLACE TABLE inventory AS SELECT * FROM inventory")
conn.execute("CREATE OR REPLACE TABLE fulfillment AS SELECT * FROM fulfillment")

print("✅ Tables loaded successfully!")
print(f"   Orders: {len(orders):,} rows")
print(f"   Inventory: {len(inventory):,} rows")
print(f"   Fulfillment: {len(fulfillment):,} rows")

conn.close()
