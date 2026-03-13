# ================================================
# Supply Chain Analytics - Automated Report Generator
# Run: python generate_report.py
# ================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import warnings
import os
warnings.filterwarnings('ignore')

print("Loading data...")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
orders = pd.read_csv('data/raw/Orders_and_shipments.csv',
                     encoding='latin-1', skipinitialspace=True)
inventory = pd.read_csv('data/raw/Inventory.csv',
                        encoding='latin-1', skipinitialspace=True)
fulfillment = pd.read_csv('data/raw/Fulfillment.csv',
                          encoding='latin-1', skipinitialspace=True)

orders.columns = orders.columns.str.strip()
inventory.columns = inventory.columns.str.strip()
fulfillment.columns = fulfillment.columns.str.strip()

orders['Discount %'] = pd.to_numeric(
    orders['Discount %'].replace(' - ', 0), errors='coerce').fillna(0)
orders.rename(columns={'Shipment Days - Scheduled': 'Shipment_Delay'}, inplace=True)
inventory['Storage Cost'] = inventory['Warehouse Inventory'] * inventory['Inventory Cost Per Unit']

# ------------------------------------------------
# CALCULATE KPIs
# ------------------------------------------------
total_revenue = orders['Gross Sales'].sum()
total_profit = orders['Profit'].sum()
profit_margin = (total_profit / total_revenue) * 100
total_orders = len(orders)
avg_delay = orders['Shipment_Delay'].mean()
delay_4_pct = (orders['Shipment_Delay'] == 4).sum() / total_orders * 100
total_storage_cost = inventory['Storage Cost'].sum()
inventory_delta = inventory['Warehouse Inventory'].sum() - orders['Order Quantity'].sum()

print("Generating charts...")

# ------------------------------------------------
# GENERATE CHARTS
# ------------------------------------------------
os.makedirs('reports', exist_ok=True)

# Chart 1 - Delay Distribution
delay_counts = orders['Shipment_Delay'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10, 5))
bar_colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
bars = ax.bar(delay_counts.index, delay_counts.values, color=bar_colors)
for bar, val in zip(bars, delay_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 150,
            f'{val:,}\n({val/total_orders*100:.1f}%)', ha='center', fontsize=10, fontweight='bold')
ax.set_title('Shipment Delay Distribution', fontsize=13, fontweight='bold')
ax.set_xlabel('Days Delayed')
ax.set_ylabel('Number of Orders')
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(['1 Day', '2 Days', '3 Days', '4 Days'])
ax.set_ylim(0, delay_counts.max() * 1.2)
plt.tight_layout()
plt.savefig('reports/chart1_shipment_delay.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 2 - Profit by Department
dept_profit = orders.groupby('Product Department')['Profit'].sum().sort_values()
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(dept_profit.index, dept_profit.values, color='#3498db')
for i, val in enumerate(dept_profit.values):
    ax.text(val + 500, i, f'${val:,.0f}', va='center', fontsize=9)
ax.set_title('Total Profit by Product Department', fontsize=13, fontweight='bold')
ax.set_xlabel('Total Profit ($)')
plt.tight_layout()
plt.savefig('reports/chart2_profit_by_department.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 3 - Stock Status
merged = orders.merge(inventory, on='Product Name', how='left')
stock_status = merged.groupby('Product Department').agg(
    avg_inventory=('Warehouse Inventory', 'mean'),
    avg_demand=('Order Quantity', 'mean')
).reset_index()
stock_status['gap'] = stock_status['avg_inventory'] - stock_status['avg_demand']
stock_status = stock_status.sort_values('gap')
fig, ax = plt.subplots(figsize=(10, 6))
colors_list = ['#e74c3c' if x < 0 else '#2ecc71' for x in stock_status['gap']]
ax.barh(stock_status['Product Department'], stock_status['gap'], color=colors_list)
ax.axvline(x=0, color='black', linewidth=1, linestyle='--')
ax.set_title('Inventory Gap by Department\n(Positive = Overstocked | Negative = Understocked)',
             fontsize=12, fontweight='bold')
ax.set_xlabel('Avg Inventory - Avg Demand (units)')
plt.tight_layout()
plt.savefig('reports/chart3_stock_status.png', dpi=150, bbox_inches='tight')
plt.close()

# Chart 4 - Top 10 Products
top_products = orders.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_products.index[::-1], top_products.values[::-1], color='#3498db')
for i, val in enumerate(top_products.values[::-1]):
    ax.text(val + 1000, i, f'${val:,.0f}', va='center', fontsize=9)
ax.set_title('Top 10 Most Profitable Products', fontsize=13, fontweight='bold')
ax.set_xlabel('Total Profit ($)')
plt.tight_layout()
plt.savefig('reports/chart4_top_products.png', dpi=150, bbox_inches='tight')
plt.close()

print("Building PDF report...")

# ------------------------------------------------
# BUILD PDF REPORT
# ------------------------------------------------
doc = SimpleDocTemplate(
    'reports/supply_chain_report.pdf',
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('title', fontSize=22, fontName='Helvetica-Bold',
                              alignment=TA_CENTER, spaceAfter=6)
subtitle_style = ParagraphStyle('subtitle', fontSize=11, fontName='Helvetica',
                                 alignment=TA_CENTER, textColor=colors.grey, spaceAfter=20)
heading_style = ParagraphStyle('heading', fontSize=14, fontName='Helvetica-Bold',
                                spaceBefore=16, spaceAfter=8)
body_style = ParagraphStyle('body', fontSize=10, fontName='Helvetica',
                             spaceAfter=6, leading=14)

story = []

# Title Page
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("End-to-End Supply Chain Analysis", title_style))
story.append(Paragraph("Business Performance, Inventory & Shipment Report", subtitle_style))
story.append(Spacer(1, 0.3*inch))

# KPI Scorecard Table
story.append(Paragraph("KPI Scorecard", heading_style))
kpi_data = [
    ['Metric', 'Value', 'Status'],
    ['Total Orders', f'{total_orders:,}', 'Informational'],
    ['Total Revenue', f'${total_revenue:,.2f}', 'Informational'],
    ['Total Profit', f'${total_profit:,.2f}', 'Informational'],
    ['Profit Margin', f'{profit_margin:.2f}%', 'Healthy'],
    ['Avg Shipment Delay', f'{avg_delay:.2f} days', 'Needs Attention'],
    ['Orders Delayed 4 Days', f'{delay_4_pct:.1f}%', 'Critical'],
    ['Total Storage Cost', f'${total_storage_cost:,.2f}', 'Informational'],
    ['Inventory Surplus', f'{inventory_delta:,} units', 'Needs Attention'],
]

kpi_table = Table(kpi_data, colWidths=[2.8*inch, 1.8*inch, 1.8*inch])
kpi_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(kpi_table)
story.append(Spacer(1, 0.3*inch))

# Key Findings
story.append(Paragraph("Key Findings", heading_style))
findings = [
    "1. 100% of orders experience shipment delays ranging from 1 to 4 days, with 58.3% experiencing the maximum 4-day delay. This indicates a systemic logistics issue.",
    "2. Fan Shop is the highest-performing department generating $1.64M in profit, followed by Apparel ($912K) and Golf ($655K).",
    "3. Apparel and Golf departments show the largest inventory surplus, indicating significant overstocking that increases carrying costs.",
    "4. The Perfect Fitness Perfect Rip Deck is the single most profitable product at $630,924 in total profit.",
    "5. Revenue and profit remained stable from 2015 to mid-2017, followed by a sharp decline in late 2017 requiring further investigation.",
]
for finding in findings:
    story.append(Paragraph(finding, body_style))

story.append(PageBreak())

# Charts
story.append(Paragraph("Analysis Charts", heading_style))
chart_files = [
    ('reports/chart1_shipment_delay.png', 'Chart 1: Shipment Delay Distribution'),
    ('reports/chart2_profit_by_department.png', 'Chart 2: Profit by Product Department'),
    ('reports/chart3_stock_status.png', 'Chart 3: Inventory Gap by Department'),
    ('reports/chart4_top_products.png', 'Chart 4: Top 10 Most Profitable Products'),
]

for chart_path, chart_title in chart_files:
    if os.path.exists(chart_path):
        story.append(Paragraph(chart_title, body_style))
        story.append(Image(chart_path, width=6.5*inch, height=3.5*inch))
        story.append(Spacer(1, 0.2*inch))

# Recommendations
story.append(PageBreak())
story.append(Paragraph("Recommendations", heading_style))
recommendations = [
    "1. Investigate Shipment Delays: All orders are delayed by 1-4 days. Conduct a root cause analysis on logistics partners, warehouse processing times, and shipping mode efficiency.",
    "2. Optimize Inventory Levels: Apparel and Golf departments are significantly overstocked. Reduce purchase orders and run targeted promotions to clear surplus inventory.",
    "3. Focus on High-Margin Products: Prioritize stock availability for top performers like Perfect Fitness Rip Deck, Field & Stream Gun Safe, and Nike Running Shoes.",
    "4. Investigate 2017 Revenue Decline: The sharp drop in late 2017 requires further analysis to determine whether it is seasonal, market-driven, or operational.",
    "5. Review Low-Profit Departments: Book Shop, Pet Shop, and Health & Beauty generate minimal profit. Evaluate whether to expand, reposition, or discontinue these product lines.",
]
for rec in recommendations:
    story.append(Paragraph(rec, body_style))

doc.build(story)
print("Report saved to reports/supply_chain_report.pdf")