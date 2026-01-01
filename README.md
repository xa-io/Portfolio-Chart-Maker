# Portfolio Chart v1.00

Advanced portfolio visualization tool for Coinbase trading data with BTC overlay capabilities.

## Overview

This script creates professional-grade charts from portfolio data including balance tracking, spending analysis, volume visualization, and optional Bitcoin price overlay. Features a dark theme with customizable display options for comprehensive portfolio performance analysis and reporting.

## Features

### Core Visualization
- **Multi-axis Portfolio Charting**: Balance, spending, and volume data on synchronized axes
- **Percentage or Dollar Display**: Toggle between percentage-based or absolute dollar values
- **Bitcoin Price Overlay**: Optional gold line showing BTC price correlation
- **Dark Theme Styling**: Professional dark background with light gray text
- **Earned Income Calculation**: Shows balance + cumulative spends as total earned income

### Customizable Display Options
- **Volume Display**: Toggle 30-day volume bars on/off
- **Spending Analysis**: Optional teal line showing spending patterns
- **Date Labels**: Show/hide date labels on x-axis
- **Balance Values**: Show/hide numeric y-axis labels
- **Grid Lines**: Toggle light gray grid lines for better readability

### Data Processing
- **CSV Data Parsing**: Reads portfolio.txt with date,balance,spends,volume,btc_price format
- **Portable File Handling**: Automatically locates portfolio.txt in script directory (no hardcoded paths)
- **Error Handling**: Comprehensive validation and error reporting
- **Automatic Export**: Saves charts with timestamped filenames in Charts/ directory
- **5% Buffer Margins**: Automatic chart scaling with visual buffers

## Requirements

```
matplotlib
```

## Installation

1. Clone this repository
2. Install required dependencies:
   ```bash
   pip install matplotlib
   ```
3. Prepare your data file (see Data Format section)

## Usage

### Quick Start

1. Create a `portfolio.txt` file in the same directory as the script
2. Run the script:
   ```bash
   python "portfolio btc.py"
   ```
3. Charts are automatically saved to the `Charts/` directory

### Configuration

Edit the configuration flags at the top of the script to customize display:

```python
# Configuration flags
SHOW_BALANCE = True          # If False, hides balance line and balance axis labels
SHOW_BALANCE_VALUES = True   # Hide/show numeric y-axis labels on the right axis (Balance+Spends)
SHOW_DATE = True             # Hide/show date labels on x-axis
BALANCE_TYPE = "Percent"     # "Dollars" or "Percent"
OVERLAY_BTC = False          # Plot BTC gold line if True
SHOW_SPENDS = False          # If False, no teal line or "Spends" text
SHOW_EARNED_INCOME = True    # If True, show the sum of balance+spends as earned income
SHOW_VOLUME = True           # If False, no volume bar or volume axis info
SHOW_GRID = True             # If True, show light gray grid lines instead of ticks
```

### Theme Customization

```python
# Theme colors
BG_COLOR = '#171b25'         # Dark background color
TEXT_COLOR = 'lightgray'     # Light gray text color
```

## Data Format

The script expects a `portfolio.txt` file with the following CSV format:

```
date,balance,spends,volume,btc_price
01/15/2024,10000.50,250.00,1500000,42000.00
01/16/2024,10150.25,125.75,1750000,43500.00
```

### Column Descriptions
- **date**: MM/DD/YYYY format
- **balance**: Portfolio balance in USD
- **spends**: Daily spending amount in USD
- **volume**: 30-day trading volume
- **btc_price**: Bitcoin price in USD

## Output

- **Chart Display**: Interactive matplotlib window
- **File Export**: Timestamped PNG files in `Charts/` directory
- **Filename Format**: `YYYY_MM_DD_-_HH_MM.png`

## Chart Elements

### Color Coding
- **Red Line**: Portfolio balance
- **Green Line/Bars**: Trading volume
- **Teal Line**: Spending analysis (optional)
- **Purple Line**: Earned income (optional)
- **Gold Line**: Bitcoin price overlay (optional)

### Axes
- **Left Y-Axis**: Volume (millions)
- **Right Y-Axis**: Balance (% or $)
- **X-Axis**: Date timeline

## Examples

### Basic Portfolio Chart (Default Settings)
```python
SHOW_BALANCE = True
SHOW_VOLUME = True
SHOW_SPENDS = False
SHOW_EARNED_INCOME = True
BALANCE_TYPE = "Percent"
OVERLAY_BTC = False
SHOW_GRID = True
```

### Full Analysis with BTC Overlay
```python
SHOW_BALANCE = True
SHOW_VOLUME = True
SHOW_SPENDS = True
SHOW_EARNED_INCOME = True
BALANCE_TYPE = "Dollars"
OVERLAY_BTC = True
SHOW_GRID = True
```

## Error Handling

- **File Not Found**: Clear error message if portfolio.txt is missing
- **Data Validation**: Skips invalid lines with detailed error reporting
- **Numeric Parsing**: Handles malformed numeric data gracefully
- **Empty Data**: Prevents crashes when no valid data is found

## Version History

### v1.00 (2025-07-29)
- Initial release with comprehensive portfolio charting capabilities
- Multi-axis visualization with balance, spending, and volume data
- Dark theme with professional styling
- Configurable display options for all chart elements
- Automatic chart export with timestamped filenames
- Bitcoin price overlay functionality
- Earned income calculation and display
- Comprehensive error handling and data validation
