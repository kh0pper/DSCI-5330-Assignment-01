#!/usr/bin/env python3
"""
Forecast Analysis for International Notion Distributors
- Remainder of 2017 forecast
- North American expansion opportunity sizing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_excel('100k.xlsx')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Quarter'] = df['Order Date'].dt.quarter
df['Profit_Margin'] = (df['Total Profit'] / df['Total Revenue']) * 100

print("="*80)
print("FORECAST ANALYSIS FOR MR. SINGH")
print("="*80)

# 1. REMAINDER OF 2017 FORECAST
print("\n1. REMAINDER OF 2017 FORECAST")
print("-" * 40)

# Analyze 2017 YTD performance
df_2017 = df[df['Year'] == 2017]
ytd_revenue = df_2017['Total Revenue'].sum()
ytd_profit = df_2017['Total Profit'].sum()
ytd_orders = len(df_2017)
last_date = df_2017['Order Date'].max()

print(f"2017 Year-to-Date (through {last_date.strftime('%B %d')}):")
print(f"  Revenue: ${ytd_revenue/1e9:.2f}B")
print(f"  Profit: ${ytd_profit/1e9:.2f}B")
print(f"  Orders: {ytd_orders:,}")
print(f"  Profit Margin: {(ytd_profit/ytd_revenue)*100:.1f}%")

# Calculate daily run rates
days_elapsed = (last_date - pd.Timestamp('2017-01-01')).days + 1
days_remaining = 365 - days_elapsed

daily_revenue_rate = ytd_revenue / days_elapsed
daily_profit_rate = ytd_profit / days_elapsed
daily_order_rate = ytd_orders / days_elapsed

print(f"\nDaily Run Rates (based on YTD):")
print(f"  Revenue: ${daily_revenue_rate/1e6:.2f}M/day")
print(f"  Profit: ${daily_profit_rate/1e6:.2f}M/day")
print(f"  Orders: {daily_order_rate:.0f}/day")

# Project remainder of year with seasonal adjustment
# Analyze historical patterns for Aug-Dec vs Jan-Jul
historical_monthly = df[df['Year'].between(2014, 2016)].groupby(['Year', 'Month'])['Total Revenue'].sum()
avg_monthly = historical_monthly.groupby('Month').mean()

# Calculate seasonal factors
jan_jul_avg = avg_monthly[avg_monthly.index <= 7].mean()
aug_dec_avg = avg_monthly[avg_monthly.index >= 8].mean()
seasonal_factor = aug_dec_avg / jan_jul_avg

print(f"\nSeasonal Pattern Analysis (2014-2016):")
print(f"  Jan-Jul average monthly revenue: ${jan_jul_avg/1e9:.2f}B")
print(f"  Aug-Dec average monthly revenue: ${aug_dec_avg/1e9:.2f}B")
print(f"  Seasonal adjustment factor: {seasonal_factor:.2f}x")

# Apply seasonal adjustment
base_remaining_revenue = daily_revenue_rate * days_remaining
adjusted_remaining_revenue = base_remaining_revenue * seasonal_factor
adjusted_remaining_profit = (daily_profit_rate * days_remaining) * seasonal_factor
adjusted_remaining_orders = int(daily_order_rate * days_remaining * seasonal_factor)

print(f"\nProjected for Remainder of 2017 (Aug-Dec, {days_remaining} days):")
print(f"  Base projection: ${base_remaining_revenue/1e9:.2f}B")
print(f"  Seasonally adjusted: ${adjusted_remaining_revenue/1e9:.2f}B")
print(f"  Projected Profit: ${adjusted_remaining_profit/1e9:.2f}B")
print(f"  Projected Orders: {adjusted_remaining_orders:,}")

# Full year projection
full_year_revenue = ytd_revenue + adjusted_remaining_revenue
full_year_profit = ytd_profit + adjusted_remaining_profit
full_year_orders = ytd_orders + adjusted_remaining_orders

print(f"\n2017 FULL YEAR FORECAST:")
print(f"  Total Revenue: ${full_year_revenue/1e9:.2f}B")
print(f"  Total Profit: ${full_year_profit/1e9:.2f}B")
print(f"  Total Orders: {full_year_orders:,}")
print(f"  Profit Margin: {(full_year_profit/full_year_revenue)*100:.1f}%")

# Compare to historical average
historical_avg = df[df['Year'].between(2014, 2016)]['Total Revenue'].groupby(df['Year']).sum().mean()
print(f"\nComparison to Recent History:")
print(f"  2014-2016 Average: ${historical_avg/1e9:.2f}B")
print(f"  2017 Forecast: ${full_year_revenue/1e9:.2f}B")
print(f"  Variance: {((full_year_revenue/historical_avg)-1)*100:+.1f}%")

# Monthly breakdown for remainder of year
print(f"\nMonthly Revenue Forecast (Aug-Dec 2017):")
for month in range(8, 13):
    month_name = pd.Timestamp(f'2017-{month:02d}-01').strftime('%B')
    month_factor = avg_monthly[month] / avg_monthly.mean()
    month_revenue = (adjusted_remaining_revenue / 5) * month_factor
    print(f"  {month_name}: ${month_revenue/1e9:.2f}B")

# 2. NORTH AMERICAN EXPANSION OPPORTUNITY
print("\n" + "="*80)
print("NORTH AMERICAN MARKET EXPANSION OPPORTUNITY ANALYSIS")
print("="*80)

# Current North American performance
df_na = df[df['Region'] == 'North America']
na_revenue = df_na['Total Revenue'].sum()
na_profit = df_na['Total Profit'].sum()
na_orders = len(df_na)
total_revenue = df['Total Revenue'].sum()
na_share = (na_revenue / total_revenue) * 100

print(f"\nCurrent North American Position (2010-2017 YTD):")
print(f"  Cumulative Revenue: ${na_revenue/1e9:.2f}B")
print(f"  Annual Revenue Run Rate: ${(na_revenue/7.58)/1e9:.2f}B")
print(f"  Market Share: {na_share:.1f}% of global revenue")
print(f"  Profit Margin: {(na_profit/na_revenue)*100:.1f}%")
print(f"  Total Orders: {na_orders:,}")

# Benchmark against other regions
regional_stats = df.groupby('Region').agg({
    'Total Revenue': 'sum',
    'Order ID': 'count',
    'Total Profit': 'sum',
    'Profit_Margin': 'mean'
}).sort_values('Total Revenue', ascending=False)

print(f"\nRegional Performance Comparison:")
print(f"{'Region':<40} {'Revenue':<12} {'Share':<8} {'Margin'}")
print("-" * 70)
for region in regional_stats.index:
    rev = regional_stats.loc[region, 'Total Revenue']
    share = (rev / total_revenue) * 100
    margin = regional_stats.loc[region, 'Profit_Margin']
    print(f"{region:<40} ${rev/1e9:>6.1f}B     {share:>5.1f}%    {margin:>5.1f}%")

# Market size context
print("\n" + "="*80)
print("NORTH AMERICAN MARKET CONTEXT")
print("="*80)
print("\nNorth America represents the world's largest consumer market:")
print("  • USA GDP: ~$21 trillion (24% of global GDP)")
print("  • Canada GDP: ~$1.7 trillion")
print("  • Combined: ~$23 trillion market")
print("\nOur current 2.2% share suggests massive untapped potential")

# Calculate expansion scenarios
print("\n" + "="*80)
print("NORTH AMERICAN EXPANSION REVENUE FORECASTS")
print("="*80)

current_na_annual = na_revenue / 7.58  # Annual run rate

print("\n📊 SCENARIO 1: CONSERVATIVE (Organic Growth)")
print("-" * 40)
year1_conservative = current_na_annual * 1.5  # 50% growth
year2_conservative = year1_conservative * 1.3  # 30% growth
year3_conservative = year2_conservative * 1.2  # 20% growth

print(f"  2017 Baseline: ${current_na_annual/1e9:.2f}B")
print(f"  2018 Forecast: ${year1_conservative/1e9:.2f}B (+50%)")
print(f"  2019 Forecast: ${year2_conservative/1e9:.2f}B (+30%)")
print(f"  2020 Forecast: ${year3_conservative/1e9:.2f}B (+20%)")
print(f"  3-Year Incremental Revenue: ${(year1_conservative + year2_conservative + year3_conservative - 3*current_na_annual)/1e9:.2f}B")

print("\n📈 SCENARIO 2: MODERATE (Strategic Partnerships)")
print("-" * 40)
year1_moderate = current_na_annual * 2.0     # Double
year2_moderate = year1_moderate * 1.5        # 50% growth
year3_moderate = year2_moderate * 1.3        # 30% growth

print(f"  2017 Baseline: ${current_na_annual/1e9:.2f}B")
print(f"  2018 Forecast: ${year1_moderate/1e9:.2f}B (+100%)")
print(f"  2019 Forecast: ${year2_moderate/1e9:.2f}B (+50%)")
print(f"  2020 Forecast: ${year3_moderate/1e9:.2f}B (+30%)")
print(f"  3-Year Incremental Revenue: ${(year1_moderate + year2_moderate + year3_moderate - 3*current_na_annual)/1e9:.2f}B")

print("\n🚀 SCENARIO 3: AGGRESSIVE (Acquisition + Expansion)")
print("-" * 40)
year1_aggressive = current_na_annual * 3.0   # Triple via acquisition
year2_aggressive = year1_aggressive * 1.5    # 50% organic growth
year3_aggressive = year2_aggressive * 1.4    # 40% growth

print(f"  2017 Baseline: ${current_na_annual/1e9:.2f}B")
print(f"  2018 Forecast: ${year1_aggressive/1e9:.2f}B (+200%)")
print(f"  2019 Forecast: ${year2_aggressive/1e9:.2f}B (+50%)")
print(f"  2020 Forecast: ${year3_aggressive/1e9:.2f}B (+40%)")
print(f"  3-Year Incremental Revenue: ${(year1_aggressive + year2_aggressive + year3_aggressive - 3*current_na_annual)/1e9:.2f}B")

# Impact on overall company (using moderate scenario)
print("\n" + "="*80)
print("IMPACT ON TOTAL COMPANY REVENUE (Moderate Scenario)")
print("="*80)

base_revenue = full_year_revenue
other_regions_revenue = base_revenue - current_na_annual

# Assume 2% organic growth in other regions
revenue_2018 = (other_regions_revenue * 1.02) + year1_moderate
revenue_2019 = (other_regions_revenue * 1.04) + year2_moderate
revenue_2020 = (other_regions_revenue * 1.06) + year3_moderate

print(f"\nTotal Company Revenue Projections:")
print(f"  2017 Baseline: ${base_revenue/1e9:.2f}B")
print(f"  2018 Forecast: ${revenue_2018/1e9:.2f}B (+{(revenue_2018/base_revenue-1)*100:.1f}%)")
print(f"  2019 Forecast: ${revenue_2019/1e9:.2f}B (+{(revenue_2019/base_revenue-1)*100:.1f}%)")
print(f"  2020 Forecast: ${revenue_2020/1e9:.2f}B (+{(revenue_2020/base_revenue-1)*100:.1f}%)")

print(f"\nNorth American Share Evolution:")
print(f"  2017: {(current_na_annual/base_revenue)*100:.1f}%")
print(f"  2018: {(year1_moderate/revenue_2018)*100:.1f}%")
print(f"  2019: {(year2_moderate/revenue_2019)*100:.1f}%")
print(f"  2020: {(year3_moderate/revenue_2020)*100:.1f}%")

# Investment and ROI
print("\n" + "="*80)
print("INVESTMENT REQUIREMENTS & ROI (Moderate Scenario)")
print("="*80)

# Investment estimates
investment_y1 = 120e6  # $120M for infrastructure, marketing, team
investment_y2 = 80e6   # $80M for expansion
investment_y3 = 60e6   # $60M for optimization
total_investment = investment_y1 + investment_y2 + investment_y3

# Profit projections (using company average margin)
avg_margin = df['Total Profit'].sum() / df['Total Revenue'].sum()
incremental_profit = ((year1_moderate - current_na_annual) + 
                     (year2_moderate - current_na_annual) + 
                     (year3_moderate - current_na_annual)) * avg_margin

roi = ((incremental_profit - total_investment) / total_investment) * 100

print(f"\nInvestment Plan:")
print(f"  Year 1 (2018): ${investment_y1/1e6:.0f}M")
print(f"    - Distribution centers: $50M")
print(f"    - Marketing & brand building: $40M")
print(f"    - Team & operations: $30M")
print(f"  Year 2 (2019): ${investment_y2/1e6:.0f}M")
print(f"    - Geographic expansion: $50M")
print(f"    - Technology & systems: $30M")
print(f"  Year 3 (2020): ${investment_y3/1e6:.0f}M")
print(f"    - Optimization & efficiency: $60M")
print(f"  Total 3-Year Investment: ${total_investment/1e6:.0f}M")

print(f"\nReturn on Investment:")
print(f"  3-Year Incremental Revenue: ${(year1_moderate + year2_moderate + year3_moderate - 3*current_na_annual)/1e9:.2f}B")
print(f"  3-Year Incremental Profit: ${incremental_profit/1e9:.2f}B")
print(f"  Total Investment: ${total_investment/1e6:.0f}M")
print(f"  ROI: {roi:.0f}%")
print(f"  Payback Period: ~{total_investment/(incremental_profit/3):.1f} years")

# Strategic recommendations
print("\n" + "="*80)
print("STRATEGIC RECOMMENDATIONS FOR NORTH AMERICAN EXPANSION")
print("="*80)

print("\n1. IMMEDIATE ACTIONS (Q4 2017):")
print("   ✓ Conduct market research on consumer preferences")
print("   ✓ Identify acquisition targets or partnership opportunities")
print("   ✓ Secure board approval for investment")
print("   ✓ Recruit North American leadership team")

print("\n2. PHASE 1 - ESTABLISH (Q1-Q2 2018):")
print("   ✓ Set up distribution centers in NYC, Chicago, LA")
print("   ✓ Launch pilot with 3 product lines in test markets")
print("   ✓ Partner with major retailers (Walmart, Target, Costco)")
print("   ✓ Build e-commerce platform for direct sales")

print("\n3. PHASE 2 - EXPAND (Q3-Q4 2018):")
print("   ✓ Roll out full product portfolio")
print("   ✓ Expand to 10 major metropolitan areas")
print("   ✓ Launch aggressive marketing campaign")
print("   ✓ Consider strategic acquisition")

print("\n4. PHASE 3 - OPTIMIZE (2019-2020):")
print("   ✓ Achieve national coverage")
print("   ✓ Optimize supply chain and logistics")
print("   ✓ Develop NA-specific products")
print("   ✓ Target 10%+ market share")

# Key success factors
print("\n5. KEY SUCCESS FACTORS:")

# Identify best products for NA market
top_products = df.groupby('Item Type')['Profit_Margin'].mean().sort_values(ascending=False).head(5)
print("\n   Product Focus (High-Margin Winners):")
for product, margin in top_products.items():
    print(f"   • {product}: {margin:.1f}% margin")

print("\n   Competitive Advantages:")
print("   • Proven global supply chain capability")
print("   • Strong balance sheet for investment")
print("   • Existing online/offline expertise")
print("   • High margins allow competitive pricing")

print("\n" + "="*80)
print("✅ Forecast Analysis Complete!")
print("="*80)