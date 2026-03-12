import duckdb
import re

conn = duckdb.connect('sql/supply_chain.db')

files = [
    'sql/shipment_delay_analysis.sql',
    'sql/inventory_turnover.sql',
    'sql/business_performance.sql',
    'sql/order_fulfillment.sql',
    'sql/supply_demand_gap.sql'
]

for filepath in files:
    print(f'\n{"="*60}')
    print(f'  {filepath}')
    print(f'{"="*60}')

    with open(filepath, 'r') as f:
        content = f.read()

    # Remove comment lines, then split by semicolon
    lines = [l for l in content.split('\n') if not l.strip().startswith('--')]
    cleaned = '\n'.join(lines)
    queries = [q.strip() for q in cleaned.split(';') if q.strip()]

    for i, query in enumerate(queries):
        if len(query) < 10:
            continue
        try:
            result = conn.execute(query).df()
            if not result.empty:
                print(f'\n[Query {i+1}]')
                print(result.to_string(index=False))
        except Exception as e:
            print(f'\n[Query {i+1}] Error: {e}')

conn.close()
print('\n✅ All queries complete!')
