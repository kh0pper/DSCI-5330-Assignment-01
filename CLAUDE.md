# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a completed DSCI-5330 business analytics assignment analyzing International Notion Distributors' (IND) performance and strategic opportunities. The project delivers executive-level business intelligence for a fictional CEO transition scenario, with 2017 data available through July 28, 2017.

## Core Analysis Architecture

### Data Pipeline Flow
```
100k.xlsx (Raw Data) → Python Analysis Scripts → Visualizations & Excel Reports → Web Presentation & Documents
```

The pipeline processes 100,000 transaction records (2010-2017) through multiple analysis engines to generate executive deliverables.

## Key Commands

### Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib seaborn openpyxl python-docx scipy
```

### Run Core Analysis
```bash
# Generate 2017 forecast and North American expansion scenarios
python north_america_expansion_analysis.py

# Create executive dashboard and strategic visualizations (3 PNG files)
python generate_charts.py

# Generate Excel workbook with calculated projections
python create_2017_projections_excel.py

# Create Excel with live formulas referencing raw data
python create_2017_projections_with_formulas.py
```

### View Web Presentation
```bash
# Local viewing
open index.html

# GitHub Pages (if enabled)
# https://[username].github.io/DSCI-5330-Assignment-01/
```

## High-Level Architecture

### Analysis Components

**Forecasting Engine** (`north_america_expansion_analysis.py`):
- Calculates daily run rates from partial 2017 data ($47.86M/day revenue)
- Applies seasonal adjustment factor (1.009x for Aug-Dec based on 2014-2016 patterns)
- Projects full-year 2017: $17.53B revenue, $5.23B profit, 29.8% margin
- Models three North American expansion scenarios with compound growth
- Generates ROI calculations (159% return on $260M investment)

**Visualization Framework** (`generate_charts.py`):
- Creates 8-panel executive dashboard (20x24 inch format, 300 DPI)
- Implements strategic matrix analysis (revenue vs margin quadrants)
- Uses consistent seaborn-v0_8-whitegrid styling with executive color schemes
- Outputs: `executive_dashboard.png`, `revenue_growth_trend.png`, `strategic_matrix.png`

**Excel Generation System**:
- `create_2017_projections_excel.py`: Static calculations with professional formatting
- `create_2017_projections_with_formulas.py`: Dynamic workbook with live Excel formulas
- Both include: Executive Summary, Detailed Calculations, Seasonal Analysis, Monthly Projections, Historical Comparison

**Web Presentation** (`index.html`):
- Professional memorandum format with IND color scheme (#2a5010, #80b122, #9cc85c)
- Embedded PowerPoint presentation via SharePoint iframe
- Interactive Tableau Public visualizations (7 embedded dashboards)
- Responsive design with print optimization

### Data Flow and Dependencies

```
Input Data:
├── 100k.xlsx (100,000 transactions, 14 columns, ends July 28, 2017)
│
Processing:
├── north_america_expansion_analysis.py
│   └── Generates console output with forecasts
├── generate_charts.py
│   └── Creates 3 strategic PNG visualizations
├── create_2017_projections_excel.py
│   └── Produces 2017_Sales_Projections_IND.xlsx
├── create_2017_projections_with_formulas.py
│   └── Produces 2017_Sales_Projections_WITH_FORMULAS.xlsx
│
Outputs:
├── Executive Dashboard (1.35MB PNG, 8 panels)
├── Strategic Charts (3 PNG files)
├── Excel Workbooks (2 versions)
├── HTML Presentation (index.html)
└── Executive Documents (Markdown memoranda)
```

### Critical Business Context

**Data Context**: 2017 data available through July 28 - analysis projects $17.53B full-year revenue
**Strategic Gap**: North America only 2.2% of revenue despite $23T market opportunity
**Investment Case**: $260M expansion investment targeting 8% NA market share with 159% ROI
**Operational Issue**: All order priorities ship in identical 25 days (service level failure)

## Architecture Insights

### Forecasting Methodology
The system uses sophisticated seasonal adjustment:
1. Calculates historical monthly averages (2014-2016)
2. Compares Jan-Jul vs Aug-Dec performance patterns
3. Derives seasonal factor (Aug-Dec revenues 0.9% higher than Jan-Jul)
4. Applies factor to daily run rates for remainder projection

### Visualization Design Patterns
- **Executive Dashboard**: 8 synchronized panels showing KPIs, trends, regional distribution, product mix
- **Strategic Matrix**: BCG-style quadrant analysis positioning products by revenue and margin
- **Growth Trends**: Year-over-year performance with color-coded positive/negative periods

### Excel Formula Architecture
The formula-based workbook creates dynamic calculations:
- Raw data sheet formatted as Excel table "TransactionData"
- Dashboard uses `SUMIFS()` and `COUNTIFS()` formulas
- Seasonal analysis uses `AVERAGE()` of monthly ranges
- All projections cascade through cell references
- Changes to raw data automatically update all calculations

### Strategic Analysis Framework
- **Regional Concentration**: Sub-Saharan Africa + Europe = 51% of revenue
- **Product Portfolio**: High-margin opportunities (Clothes 67%, Cereal 43%) vs low-margin volume drivers
- **Expansion Modeling**: Three scenarios (Conservative +50%, Moderate +100%, Aggressive +200% Year 1 growth)
- **Service Differentiation**: Priority-based fulfillment recommendations

## File Dependencies

**Required Input**:
- `100k.xlsx` - Core transaction dataset (must exist for all scripts)

**Generated Outputs**:
- PNG visualizations: 3 strategic charts + 7 additional dashboard images
- Excel workbooks: Static calculations + dynamic formula version
- Web presentation: `index.html` with embedded visualizations
- Documentation: Executive memorandum, presentation outline, speaker notes

**Color Palette** (IND Corporate Colors):
- Primary: #2a5010 (dark green)
- Secondary: #80b122 (bright green)  
- Tertiary: #3f7819 (medium green)
- Accent: #9cc85c (light green)

## Important Implementation Notes

### Data Handling
- All scripts handle the July 28, 2017 data cutoff correctly
- Seasonal patterns are calculated from complete years (2014-2016) only
- Profit margins are calculated as Total Profit / Total Revenue

### Performance Considerations
- Dataset contains 100,000 records requiring ~100MB memory
- Chart generation creates high-resolution outputs (300 DPI)
- Excel formula version includes complete dataset (11MB file)

### Output Quality
- Visualizations optimized for executive presentation
- Excel formatting uses professional business standards
- Web interface responsive and print-friendly

The codebase represents a production-ready business analytics solution demonstrating advanced forecasting, visualization design, and executive communication capabilities.