# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a completed DSCI-5330 business analytics assignment analyzing International Notion Distributors' performance and strategic opportunities. The project consists of executive-level business intelligence deliverables including forecasting, expansion analysis, and strategic recommendations for a fictional CEO transition scenario.

## Core Analysis Architecture

### Data Pipeline Flow
1. **Data Source**: `100k.xlsx` contains 100,000 transaction records (2010-2017) with 14 columns including regional, product, channel, and financial data
2. **Analysis Engine**: `north_america_expansion_analysis.py` performs comprehensive financial forecasting and expansion modeling
3. **Visualization Engine**: `generate_charts.py` creates executive-level dashboards and strategic charts
4. **Output**: Professional business documents and visualizations for C-level presentation

### Key Analysis Components

**Forecasting Logic** (`north_america_expansion_analysis.py`):
- Handles partial 2017 data (ends July 28) with seasonal adjustment factors
- Applies daily run rates with historical seasonal patterns (2014-2016 baseline)
- Generates three expansion scenarios using compound growth modeling
- Calculates ROI and payback periods for $260M investment over 3 years

**Visualization Framework** (`generate_charts.py`):
- Uses seaborn-v0_8-whitegrid styling with professional color palettes
- Creates multi-panel dashboards (20x24 inch format for executive presentation)
- Implements strategic matrix plotting (revenue vs margin quadrant analysis)
- Generates three core chart types: executive dashboard, growth trends, portfolio matrix

## Key Commands

### Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib seaborn openpyxl python-docx scipy
```

### Run Analysis
```bash
# Generate complete forecast and expansion analysis
python north_america_expansion_analysis.py

# Create all visualizations (3 PNG files)
python generate_charts.py
```

## Critical Business Context

**Data Reality Check**: The apparent "2017 revenue crisis" is actually incomplete data (only through July 28, 2017). The analysis correctly identifies this and projects full-year 2017 revenue of $17.53B, consistent with historical performance.

**Strategic Opportunity**: North America represents only 2.2% of revenue despite being the world's largest consumer market. The expansion analysis models growing this to 8% market share with 159% ROI.

**Financial Projections**: Three scenarios modeled - Conservative (+50% annual growth), Moderate (+100%/+50%/+30%), and Aggressive (+200%/+50%/+40%) for North American expansion.

## File Dependencies

- `100k.xlsx` must be present for both analysis scripts
- Both Python scripts are standalone and can run independently
- Generated PNG files are referenced in presentation materials
- All analysis assumes data through July 28, 2017 with seasonal extrapolation

## Output Files Generated

- `executive_dashboard.png` (1.3MB) - 8-panel comprehensive dashboard
- `revenue_growth_trend.png` (144KB) - Year-over-year growth analysis  
- `strategic_matrix.png` (298KB) - Product portfolio positioning

The analysis pipeline is designed for one-time execution to generate final deliverables rather than iterative development.