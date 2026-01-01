############################################################################################################################
#
#  ██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ ██╗     ██╗ ██████╗     ██████╗██╗  ██╗ █████╗ ██████╗ ████████╗
#  ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔═══██╗██║     ██║██╔═══██╗   ██╔════╝██║  ██║██╔══██╗██╔══██╗╚══██╔══╝
#  ██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██║   ██║██║     ██║██║   ██║   ██║     ███████║███████║██████╔╝   ██║   
#  ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██║   ██║██║     ██║██║   ██║   ██║     ██╔══██║██╔══██║██╔══██╗   ██║   
#  ██║     ╚██████╔╝██║  ██║   ██║   ██║     ╚██████╔╝███████╗██║╚██████╔╝   ╚██████╗██║  ██║██║  ██║██║  ██║   ██║   
#  ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚═╝ ╚═════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                         
#
# Advanced portfolio visualization tool for Coinbase trading data with BTC overlay capabilities.
#
# This script creates professional-grade charts from portfolio data including balance tracking, spending analysis,
# volume visualization, and optional Bitcoin price overlay. Features a dark theme with customizable display options
# for comprehensive portfolio performance analysis and reporting.
#
# Core Features:
# • Multi-axis portfolio charting with balance, spending, and volume data
# • Percentage or dollar-based balance display modes
# • Optional Bitcoin price overlay with gold line visualization
# • Dark theme with professional styling and grid options
# • Earned income calculation and display (balance + cumulative spends)
# • Configurable chart elements (volume, spends, dates, grid)
# • Automatic chart export with timestamped filenames
# • CSV data parsing with error handling and validation
#
# Important Note: Requires portfolio.txt data file with date,balance,spends,volume,btc_price format.
#  - Example lines: 
#    01/01/2025,1000,1.25,50000,100000.00
#    01/02/2025,1200,0,60000,105000.00
# Customize display options using configuration flags at the top of the script.
#
# Portfolio Chart v1.00
# Advanced portfolio visualization tool for Coinbase trading data
# Created by: https://github.com/xa-io
# Last Updated: 2025-07-29 08:51:00
#
# ## Release Notes ##
#
# v1.00 - Initial release with comprehensive portfolio charting capabilities
#
############################################################################################################################

#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

# Configuration flags
SHOW_BALANCE = True          # If False, hides balance line and balance axis labels
SHOW_BALANCE_VALUES = True   # Hide/show numeric y-axis labels on the right axis (Balance+Spends)
SHOW_DATE = True             # Hide/show date labels on x-axis
BALANCE_TYPE = "Percent"     # "Dollars" or "Percent"
OVERLAY_BTC = False          # Plot BTC gold line if True
SHOW_SPENDS = False          # If False, no blue line or "Spends" text
SHOW_EARNED_INCOME = True   # If True, show the sum of balance+spends as earned income
SHOW_VOLUME = True           # If False, no volume bar or volume axis info
SHOW_GRID = True             # If True, show light gray grid lines instead of ticks

# Theme colors
BG_COLOR = '#171b25'         # Dark background color (RGB: rgba(23,27,37,255))
TEXT_COLOR = 'lightgray'     # Light gray text color for all non-data text

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(script_dir, "portfolio.txt")
    
    dates = []
    balances_raw = []
    spends_raw = []
    volumes_raw = []
    btc_prices = []

    # 1) Read data with 5 columns: date,balance,spends,volume,btc_price
    try:
        with open(input_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) != 5:
                    print(f"Skipping line (expected 5 columns): {line}")
                    continue

                date_str, bal_str, sp_str, vol_str, btc_str = parts
                try:
                    date_obj = datetime.strptime(date_str.strip(), '%m/%d/%Y')
                    b        = float(bal_str.strip())
                    s        = float(sp_str.strip())
                    v        = float(vol_str.strip())
                    btc      = float(btc_str.strip())
                except ValueError:
                    print(f"Could not parse numeric fields on line: {line}")
                    continue

                dates.append(date_obj)
                balances_raw.append(b)
                spends_raw.append(s)
                volumes_raw.append(v)
                btc_prices.append(btc)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return

    if not dates:
        print("No valid data found. Exiting.")
        return
    
    # 2) Convert balance/spends if Percent
    if BALANCE_TYPE == "Percent":
        base_balance = balances_raw[0]
        if base_balance == 0:
            print("Warning: First balance is 0; using raw balances.")
            balances_plot = balances_raw[:]
            balance_label_part = "($)"
            spends_plot = spends_raw[:]
            # Calculate earned income (balance + cumulative spends)
            if SHOW_EARNED_INCOME:
                cumulative_spends = []
                total_spends = 0
                for s in spends_raw:
                    total_spends += s
                    cumulative_spends.append(total_spends)
                earned_income_plot = [b + cs for b, cs in zip(balances_raw, cumulative_spends)]
        else:
            balances_plot = [((b - base_balance) / base_balance) * 100 for b in balances_raw]
            balance_label_part = "(%)"
            if SHOW_SPENDS:
                spends_plot = []
                for i, s in enumerate(spends_raw):
                    day_balance = balances_raw[i]
                    if day_balance != 0:
                        spends_plot.append((s / day_balance) * 100)
                    else:
                        spends_plot.append(0.0)
                
                # Calculate earned income (balance + cumulative spends) in percentage
                if SHOW_EARNED_INCOME:
                    # Calculate cumulative spends
                    cumulative_spends = []
                    total_spends = 0
                    for s in spends_raw:
                        total_spends += s
                        cumulative_spends.append(total_spends)
                    
                    earned_income_raw = [b + cs for b, cs in zip(balances_raw, cumulative_spends)]
                    earned_income_plot = [((ei - base_balance) / base_balance) * 100 for ei in earned_income_raw]
            else:
                spends_plot = []
                            # Even without showing spends line, we can calculate earned income
                if SHOW_EARNED_INCOME:
                    # Calculate cumulative spends
                    cumulative_spends = []
                    total_spends = 0
                    for s in spends_raw:
                        total_spends += s
                        cumulative_spends.append(total_spends)
                        
                    earned_income_raw = [b + cs for b, cs in zip(balances_raw, cumulative_spends)]
                    earned_income_plot = [((ei - base_balance) / base_balance) * 100 for ei in earned_income_raw]
    else:
        # "Dollars"
        balances_plot = balances_raw[:]
        balance_label_part = "($)"
        if SHOW_SPENDS:
            spends_plot = spends_raw[:]
            # Calculate earned income (balance + cumulative spends) in dollars
            if SHOW_EARNED_INCOME:
                cumulative_spends = []
                total_spends = 0
                for s in spends_raw:
                    total_spends += s
                    cumulative_spends.append(total_spends)
                earned_income_plot = [b + cs for b, cs in zip(balances_raw, cumulative_spends)]
        else:
            spends_plot = []
            # Even without showing spends line, we can calculate earned income
            if SHOW_EARNED_INCOME:
                cumulative_spends = []
                total_spends = 0
                for s in spends_raw:
                    total_spends += s
                    cumulative_spends.append(total_spends)
                earned_income_plot = [b + cs for b, cs in zip(balances_raw, cumulative_spends)]

    # 3) Convert volume to millions
    volumes_millions = [v / 1_000_000 for v in volumes_raw]

    # 4) Create figure
    fig, ax_volume = plt.subplots()
    fig.subplots_adjust(right=0.73)
    
    # Set background color to dark theme and text to light gray
    fig.set_facecolor(BG_COLOR)
    ax_volume.set_facecolor(BG_COLOR)

    # Left axis -> Volume (if enabled)
    ax_volume.set_xlabel("Date", color=TEXT_COLOR)
    if SHOW_VOLUME:
        ax_volume.set_ylabel("Volume (30-day) (per millions)", color="green")
        ax_volume.plot(dates, volumes_millions, color="green")
        ax_volume.tick_params(axis="y", labelcolor="green")
        # Set x-axis tick colors to light gray
        ax_volume.tick_params(axis="x", colors=TEXT_COLOR)
    else:
        # Hide volume axis labels when volume is disabled
        ax_volume.set_yticks([])
        ax_volume.set_ylabel("")
        
    # Will configure grid after setting up both axes
    
    ax_volume.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%Y"))
    ax_volume.xaxis.set_major_locator(mdates.AutoDateLocator())

    # 5% buffer for volume (if enabled)
    if SHOW_VOLUME:
        if volumes_millions:
            vmin = min(volumes_millions)
            vmax = max(volumes_millions)
            if vmin == vmax:
                vmin -= 1
                vmax += 1
            else:
                margin = 0.05 * (vmax - vmin)
                vmin -= margin
                vmax += margin
            vmin = max(vmin, 0)
            ax_volume.set_ylim(vmin, vmax)
        else:
            ax_volume.set_ylim(0, 1)

    # Right axis -> Balance (red) + optional Spends (blue)
    ax_bal_spends = ax_volume.twinx()
    
    # Set the ylabel for the balance axis similar to volume axis (if enabled)
    if SHOW_BALANCE:
        ax_bal_spends.set_ylabel(f"Balance {balance_label_part}", color="red")
        ax_bal_spends.plot(dates, balances_plot, color="red")
    elif SHOW_EARNED_INCOME:
        # Show balance axis label if earned income is displayed (even without balance line)
        ax_bal_spends.set_ylabel(f"Balance {balance_label_part}", color="red")
    else:
        # Hide balance axis labels when balance and earned income are both disabled
        ax_bal_spends.set_ylabel("")

    if SHOW_SPENDS and spends_plot:
        ax_bal_spends.plot(dates, spends_plot, color="teal", linewidth=1.0, alpha=0.9)
        
        # "Spends" label inside chart
        ax_volume.text(
            0.02, 0.92,
            "Spends",
            color="teal",
            transform=ax_volume.transAxes,
            ha="left",
            va="top",
            fontsize=12
            # fontweight="bold"
        )
        
    # Add earned income line if enabled
    if SHOW_EARNED_INCOME and 'earned_income_plot' in locals():
        ax_bal_spends.plot(dates, earned_income_plot, color="purple", linewidth=1.0, alpha=0.9, linestyle='-')
        
        # "Earned Income" label inside chart
        position_y = 0.87 if SHOW_SPENDS else 0.92  # Adjust position if no spends shown
        ax_volume.text(
            0.02, position_y,
            "Earned Income",
            color="purple",
            transform=ax_volume.transAxes,
            ha="left",
            va="top",
            fontsize=12,
            # fontweight="bold"
        )

    # Set tick parameters for balance axis
    ax_bal_spends.tick_params(axis='y', labelcolor='red')
    
    # Update spines for balance axis to match dark theme
    for spine in ax_bal_spends.spines.values():
        spine.set_color(TEXT_COLOR)
    
    # Hide the right spine (black line on the right side)
    ax_bal_spends.spines['right'].set_visible(False)

    # combine & buffer
    combined = []
    if SHOW_BALANCE:
        combined = balances_plot[:]
    if SHOW_SPENDS and spends_plot:
        combined.extend(spends_plot)
    if SHOW_EARNED_INCOME and 'earned_income_plot' in locals():
        combined.extend(earned_income_plot)

    if combined:
        rmin = min(combined)
        rmax = max(combined)
        if rmin == rmax:
            rmin -= 1
            rmax += 1
        else:
            margin = 0.05 * (rmax - rmin)
            rmin -= margin
            rmax += margin
        if BALANCE_TYPE == "Dollars" and rmin > 0:
            rmin = max(0, rmin)
        ax_bal_spends.set_ylim(rmin, rmax)
    else:
        ax_bal_spends.set_ylim(0,1)

    fig.autofmt_xdate()
    if not SHOW_DATE:
        ax_volume.set_xticklabels([])

    if not SHOW_BALANCE_VALUES:
        ax_bal_spends.set_yticklabels([])
        
    # Configure grid based on SHOW_GRID setting (after both axes are configured)
    if SHOW_GRID:
        # Show grid lines with light gray color and 20% opacity that align with both axes
        # Use ax_volume for x-grid and ax_bal_spends for y-grid to ensure proper alignment
        ax_volume.grid(which='both', axis='x', color=TEXT_COLOR, alpha=0.2, linestyle='-', linewidth=0.5)
        ax_bal_spends.grid(which='both', axis='y', color=TEXT_COLOR, alpha=0.2, linestyle='-', linewidth=0.5)
        
        # Hide the tick marks but keep the labels for both axes
        ax_volume.tick_params(axis='both', which='both', length=0)
        ax_bal_spends.tick_params(axis='both', which='both', length=0)
    else:
        # No grid, default ticks
        ax_volume.grid(False)
        ax_bal_spends.grid(False)

    # OVERLAY BTC if True
    if OVERLAY_BTC:
        ax_btc = ax_volume.twinx()
        ax_btc.set_yticks([])
        ax_btc.set_ylabel("")
        
        # Update spines for BTC axis to match dark theme
        for spine in ax_btc.spines.values():
            spine.set_color(TEXT_COLOR)
        ax_btc.plot(dates, btc_prices, color="gold", linewidth=1.0, alpha=0.5)
        
        # Position the BTC axis to the right of the balance axis
        ax_btc.spines['right'].set_position(('outward', 60))
        
        # Hide the right spine for the BTC axis as well
        ax_btc.spines['right'].set_visible(False)

        # "BTC" label inside chart
        ax_volume.text(
            0.02, 0.97,
            "BTC",
            color="gold",
            transform=ax_volume.transAxes,
            ha="left",
            va="top",
            fontsize=12,
            # fontweight="bold"
        )

    # Dynamically build the figure title
    if SHOW_VOLUME:
        title_str = f"Portfolio Chart: Volume vs. Balance"
    else:
        title_str = f"Portfolio Chart: Balance"
        
    # Set spine colors to light gray
    for spine in ax_volume.spines.values():
        spine.set_color(TEXT_COLOR)
    
    # Set x-axis tick label color to light gray (for dates)
    ax_volume.tick_params(axis='x', labelcolor=TEXT_COLOR)

    plt.title(title_str, color=TEXT_COLOR)
    plt.tight_layout()

    # Get current date and time for the filename in the format yyyy_mm_dd_-_hh_mm.png
    now = datetime.now()
    filename = now.strftime("%Y_%m_%d_-_%H_%M.png")

    # Build the absolute path to save the file in the same directory as this script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    charts_dir = os.path.join(script_dir, "Charts")
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    filepath = os.path.join(charts_dir, filename)

    # Save figure with transparent=False to ensure background color is included
    plt.savefig(filepath, transparent=False)
    print(f"Chart saved as '{filepath}'.")
    plt.show()

if __name__=="__main__":
    main()
