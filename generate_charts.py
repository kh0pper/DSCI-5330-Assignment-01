#!/usr/bin/env python3
"""
International Notion Distributors - Data Visualizations
Creating compelling charts for executive presentation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set up professional styling
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 11

# Load data
print("Loading data and preparing visualizations...")
df = pd.read_excel('100k.xlsx')

# Convert dates and add calculated fields
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df['Year'] = df['Order Date'].dt.year
df['Quarter'] = df['Order Date'].dt.quarter
df['Month'] = df['Order Date'].dt.month
df['Year_Month'] = df['Order Date'].dt.to_period('M')
df['Profit_Margin'] = (df['Total Profit'] / df['Total Revenue']) * 100
df['Fulfillment_Days'] = (df['Ship Date'] - df['Order Date']).dt.days

# Create a figure with multiple subplots for comprehensive dashboard
fig = plt.figure(figsize=(20, 24))
fig.suptitle('International Notion Distributors - Executive Dashboard\nOctober 2017', 
             fontsize=20, fontweight='bold', y=0.995)

# 1. Revenue & Profit Trend Over Time
ax1 = plt.subplot(4, 2, 1)
yearly_data = df.groupby('Year').agg({
    'Total Revenue': 'sum',
    'Total Profit': 'sum'
})
years = yearly_data.index
x_pos = np.arange(len(years))
width = 0.35

bars1 = ax1.bar(x_pos - width/2, yearly_data['Total Revenue']/1e9, width, 
                label='Revenue', color='#3498db', alpha=0.8)
bars2 = ax1.bar(x_pos + width/2, yearly_data['Total Profit']/1e9, width,
                label='Profit', color='#2ecc71', alpha=0.8)

ax1.set_xlabel('Year')
ax1.set_ylabel('Amount (Billions $)')
ax1.set_title('Revenue & Profit Trends (2010-2017)', fontweight='bold', pad=10)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(years)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'${height:.1f}B', ha='center', va='bottom', fontsize=9)

# 2. Regional Revenue Distribution (Pie Chart)
ax2 = plt.subplot(4, 2, 2)
regional_revenue = df.groupby('Region')['Total Revenue'].sum().sort_values(ascending=False)
colors = plt.cm.Set3(np.linspace(0, 1, len(regional_revenue)))

wedges, texts, autotexts = ax2.pie(regional_revenue.values, 
                                    labels=regional_revenue.index,
                                    colors=colors,
                                    autopct='%1.1f%%',
                                    startangle=45)
ax2.set_title('Revenue Distribution by Region', fontweight='bold', pad=20)

# Make percentage text more readable
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(9)

# 3. Product Performance Matrix
ax3 = plt.subplot(4, 2, 3)
product_data = df.groupby('Item Type').agg({
    'Total Revenue': 'sum',
    'Total Profit': 'sum',
    'Profit_Margin': 'mean'
}).sort_values('Total Profit', ascending=True)

y_pos = np.arange(len(product_data))
ax3.barh(y_pos, product_data['Total Profit']/1e6, color='#9b59b6', alpha=0.8)
ax3.set_yticks(y_pos)
ax3.set_yticklabels(product_data.index, fontsize=10)
ax3.set_xlabel('Total Profit (Millions $)')
ax3.set_title('Product Portfolio Profitability', fontweight='bold', pad=10)
ax3.grid(axis='x', alpha=0.3)

# Add value labels
for i, v in enumerate(product_data['Total Profit']/1e6):
    ax3.text(v + 10, i, f'${v:.0f}M', va='center', fontsize=9)

# 4. Sales Channel Comparison
ax4 = plt.subplot(4, 2, 4)
channel_data = df.groupby('Sales Channel').agg({
    'Total Revenue': 'sum',
    'Total Profit': 'sum',
    'Order ID': 'count'
})

channels = channel_data.index
metrics = ['Revenue', 'Profit', 'Orders']
online_values = [
    channel_data.loc['Online', 'Total Revenue']/1e9,
    channel_data.loc['Online', 'Total Profit']/1e9,
    channel_data.loc['Online', 'Order ID']/1000
]
offline_values = [
    channel_data.loc['Offline', 'Total Revenue']/1e9,
    channel_data.loc['Offline', 'Total Profit']/1e9,
    channel_data.loc['Offline', 'Order ID']/1000
]

x_pos = np.arange(len(metrics))
width = 0.35

ax4.bar(x_pos - width/2, online_values, width, label='Online', color='#e74c3c', alpha=0.8)
ax4.bar(x_pos + width/2, offline_values, width, label='Offline', color='#34495e', alpha=0.8)

ax4.set_xlabel('Metrics')
ax4.set_ylabel('Value')
ax4.set_title('Online vs Offline Channel Performance', fontweight='bold', pad=10)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(['Revenue ($B)', 'Profit ($B)', 'Orders (K)'])
ax4.legend()
ax4.grid(axis='y', alpha=0.3)

# 5. Top 15 Countries by Revenue
ax5 = plt.subplot(4, 2, 5)
top_countries = df.groupby('Country')['Total Revenue'].sum().sort_values(ascending=False).head(15)
ax5.bar(range(len(top_countries)), top_countries.values/1e6, color='#16a085', alpha=0.8)
ax5.set_xlabel('Country')
ax5.set_ylabel('Revenue (Millions $)')
ax5.set_title('Top 15 Countries by Revenue', fontweight='bold', pad=10)
ax5.set_xticks(range(len(top_countries)))
ax5.set_xticklabels(top_countries.index, rotation=45, ha='right')
ax5.grid(axis='y', alpha=0.3)

# 6. Profit Margin by Product Category
ax6 = plt.subplot(4, 2, 6)
margin_data = df.groupby('Item Type')['Profit_Margin'].mean().sort_values(ascending=False)
colors_margin = ['#2ecc71' if x > 35 else '#e74c3c' if x < 25 else '#f39c12' 
                 for x in margin_data.values]

ax6.bar(range(len(margin_data)), margin_data.values, color=colors_margin, alpha=0.8)
ax6.set_xlabel('Item Type')
ax6.set_ylabel('Profit Margin (%)')
ax6.set_title('Average Profit Margin by Product Type', fontweight='bold', pad=10)
ax6.set_xticks(range(len(margin_data)))
ax6.set_xticklabels(margin_data.index, rotation=45, ha='right')
ax6.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='30% Target')
ax6.grid(axis='y', alpha=0.3)
ax6.legend()

# 7. Monthly Revenue Pattern (Last 2 Years)
ax7 = plt.subplot(4, 2, 7)
recent_data = df[df['Year'] >= 2016]
monthly_revenue = recent_data.groupby('Year_Month')['Total Revenue'].sum()

# Convert to proper format for plotting
months = [str(m) for m in monthly_revenue.index]
values = monthly_revenue.values / 1e6

ax7.plot(range(len(months)), values, marker='o', linewidth=2, 
         markersize=6, color='#8e44ad', alpha=0.8)
ax7.fill_between(range(len(months)), values, alpha=0.3, color='#8e44ad')
ax7.set_xlabel('Month')
ax7.set_ylabel('Revenue (Millions $)')
ax7.set_title('Monthly Revenue Trend (2016-2017)', fontweight='bold', pad=10)
ax7.set_xticks(range(0, len(months), 3))
ax7.set_xticklabels(months[::3], rotation=45, ha='right')
ax7.grid(True, alpha=0.3)

# 8. Fulfillment Performance by Region
ax8 = plt.subplot(4, 2, 8)
fulfillment_data = df.groupby('Region')['Fulfillment_Days'].mean().sort_values()
colors_fulfillment = ['#2ecc71' if x < 24 else '#e74c3c' if x > 26 else '#f39c12' 
                      for x in fulfillment_data.values]

ax8.barh(range(len(fulfillment_data)), fulfillment_data.values, 
         color=colors_fulfillment, alpha=0.8)
ax8.set_ylabel('Region')
ax8.set_xlabel('Average Fulfillment Days')
ax8.set_title('Fulfillment Efficiency by Region', fontweight='bold', pad=10)
ax8.set_yticks(range(len(fulfillment_data)))
ax8.set_yticklabels(fulfillment_data.index, fontsize=9)
ax8.axvline(x=25, color='red', linestyle='--', alpha=0.5, label='25 Days Target')
ax8.grid(axis='x', alpha=0.3)
ax8.legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.savefig('executive_dashboard.png', dpi=300, bbox_inches='tight')
print("✅ Executive dashboard saved as 'executive_dashboard.png'")

# Create additional focused charts for presentation

# Chart 1: Year-over-Year Growth Rate
fig2, ax = plt.subplots(1, 1, figsize=(12, 6))
yearly_growth = df.groupby('Year')['Total Revenue'].sum().pct_change() * 100
ax.plot(yearly_growth.index[1:], yearly_growth.values[1:], 
        marker='o', linewidth=3, markersize=10, color='#e74c3c')
ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax.fill_between(yearly_growth.index[1:], yearly_growth.values[1:], 0, 
                where=(yearly_growth.values[1:] >= 0), color='green', alpha=0.3)
ax.fill_between(yearly_growth.index[1:], yearly_growth.values[1:], 0,
                where=(yearly_growth.values[1:] < 0), color='red', alpha=0.3)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Growth Rate (%)', fontsize=12)
ax.set_title('Year-over-Year Revenue Growth Rate', fontsize=14, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3)

# Add value labels
for i, (year, value) in enumerate(zip(yearly_growth.index[1:], yearly_growth.values[1:])):
    ax.text(year, value + 1.5 if value >= 0 else value - 1.5, 
            f'{value:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('revenue_growth_trend.png', dpi=300, bbox_inches='tight')
print("✅ Revenue growth trend saved as 'revenue_growth_trend.png'")

# Chart 2: Strategic Priority Matrix
fig3, ax = plt.subplots(1, 1, figsize=(12, 8))
product_scatter = df.groupby('Item Type').agg({
    'Total Revenue': 'sum',
    'Profit_Margin': 'mean'
})

# Create scatter plot
scatter = ax.scatter(product_scatter['Total Revenue']/1e9, 
                    product_scatter['Profit_Margin'],
                    s=300, alpha=0.6, c=range(len(product_scatter)),
                    cmap='viridis', edgecolors='black', linewidth=2)

# Add labels
for idx, row in product_scatter.iterrows():
    ax.annotate(idx, (row['Total Revenue']/1e9, row['Profit_Margin']),
                ha='center', va='center', fontsize=9, fontweight='bold')

# Add quadrant lines
ax.axhline(y=product_scatter['Profit_Margin'].median(), 
          color='red', linestyle='--', alpha=0.5)
ax.axvline(x=product_scatter['Total Revenue'].sum()/len(product_scatter)/1e9,
          color='red', linestyle='--', alpha=0.5)

# Add quadrant labels
ax.text(0.95, 0.95, 'Stars\n(High Revenue, High Margin)', 
       transform=ax.transAxes, ha='right', va='top',
       bbox=dict(boxstyle='round', facecolor='green', alpha=0.3))
ax.text(0.05, 0.95, 'Question Marks\n(Low Revenue, High Margin)',
       transform=ax.transAxes, ha='left', va='top',
       bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
ax.text(0.95, 0.05, 'Cash Cows\n(High Revenue, Low Margin)',
       transform=ax.transAxes, ha='right', va='bottom',
       bbox=dict(boxstyle='round', facecolor='blue', alpha=0.3))
ax.text(0.05, 0.05, 'Dogs\n(Low Revenue, Low Margin)',
       transform=ax.transAxes, ha='left', va='bottom',
       bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))

ax.set_xlabel('Total Revenue (Billions $)', fontsize=12)
ax.set_ylabel('Average Profit Margin (%)', fontsize=12)
ax.set_title('Product Portfolio Strategic Matrix', fontsize=14, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('strategic_matrix.png', dpi=300, bbox_inches='tight')
print("✅ Strategic matrix saved as 'strategic_matrix.png'")

print("\n✅ All visualizations created successfully!")
print("\nFiles generated:")
print("  1. executive_dashboard.png - Comprehensive 8-panel dashboard")
print("  2. revenue_growth_trend.png - Year-over-year growth analysis")
print("  3. strategic_matrix.png - Product portfolio strategic positioning")