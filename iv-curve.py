#!/usr/bin/env python3
"""
Current Sweep Test Script for MP71077x/Korad KEL20x0 electronic loads.
This script sets the load to constant current (CC) mode, increments
the current in steps, measures the voltage after each step,
and generates a current-voltage plot.
"""
import MP71077x
import time
import argparse
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import re
import os

# Parse command line arguments
parser = argparse.ArgumentParser(description='Current Sweep Test with Plot for MP71077x/Korad KEL20x0 electronic load')
parser.add_argument('--target-ip', '-t', required=True, help='IP address of the electronic load')
parser.add_argument('--verbose', '-v', action='store_true', default=True, help='Enable verbose output')
parser.add_argument('--start-current', type=float, default=0.0, help='Starting current in amps (default: 0.0)')
parser.add_argument('--end-current', type=float, default=1.0, help='End current in amps (default: 1.0)')
parser.add_argument('--step', type=float, default=0.05, help='Current increment step in amps (default: 0.05)')
parser.add_argument('--delay', type=float, default=0.5, help='Delay between steps in seconds (default: 0.5)')
parser.add_argument('--output', '-o', help='Output file name (default: auto-generated)')
parser.add_argument('--title', help='Plot title (default: "Current-Voltage Characteristic")')
parser.add_argument('--dut', help='Device Under Test name for the plot')
args = parser.parse_args()

# Get target IP
target_ip = args.target_ip

# Initialize the load
load = MP71077x.MP71077x(target_ip=target_ip, verbosity=args.verbose)
load.openSocket()

# Lists to store data
currents = []
voltages = []
powers = []
resistances = []

try:
    # Set upper current limit slightly above our max current
    max_current = max(args.start_current, args.end_current) + 0.1
    load.setUpperCurrentLimit(max_current)

    # Set initial current
    current = args.start_current
    load.setCIcurrent(current, True)

    # Turn on the load
    load.turnInputON(True)
    print(f"Load input turned ON, starting current sweep from {args.start_current}A to {args.end_current}A")

    # Print header for data
    print(f"\n{'Current (A)':<12} | {'Voltage (V)':<12} | {'Power (W)':<12} | {'Resistance (Ω)':<12}")
    print("----------------|----------------|----------------|----------------")

    # Determine step direction
    step = args.step if args.end_current >= args.start_current else -args.step

    # Perform the current sweep
    # Add a small adjustment to include the end point
    end_test = args.end_current + (0.01 * step)

    while (step > 0 and current <= end_test) or (step < 0 and current >= end_test):
        # Set the current
        load.setCIcurrent(current, True)

        # Wait for the specified delay
        time.sleep(args.delay)

        # Measure the voltage
        voltage_str = load.sendCommand(":MEAS:VOLT?", True)
        # Clean up the string and convert to float (remove "V" and whitespace)
        voltage = float(re.sub(r'[^\d.]', '', voltage_str))

        # Calculate power and resistance
        power = current * voltage
        resistance = voltage / current if current != 0 else float('inf')

        # Store the data
        currents.append(current)
        voltages.append(voltage)
        powers.append(power)
        resistances.append(resistance if resistance != float('inf') else 0)

        # Print the data
        print(f"{current:<12.3f} | {voltage:<12.3f} | {power:<12.3f} | {resistance:<12.3f}")

        # Increment the current
        current += step

    # Turn off the load
    # First set current back to 0
    load.setCIcurrent(0.0, True)
    print("Current set back to 0.0A")

    load.turnInputOFF(True)
    print("\nCurrent sweep complete. Load input turned OFF.")

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot voltage vs current (IV curve)
    color = 'tab:blue'
    ax1.set_xlabel('Current (A)')
    ax1.set_ylabel('Voltage (V)', color=color)
    ax1.plot(currents, voltages, 'o-', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Add a second y-axis for power
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Power (W)', color=color)
    ax2.plot(currents, powers, 's-', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Add grid
    ax1.grid(True, linestyle='--', alpha=0.7)

    # Add title
    title = args.title if args.title else "Current-Voltage Characteristic"
    if args.dut:
        title += f" of {args.dut}"
    plt.title(title)

    # Add timestamp and test info
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.figtext(0.5, 0.01, f"Test performed on {timestamp}",
                ha="center", fontsize=9, style='italic')

    # Improve layout
    fig.tight_layout(pad=3)

    # Create a unique filename if not specified
    if args.output:
        output_file = args.output
    else:
        timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
        dut_part = f"_{args.dut.replace(' ', '_')}" if args.dut else ""
        output_file = f"iv_curve{dut_part}_{timestamp_file}.png"

    # Save the plot
    plt.savefig(output_file, dpi=300)
    print(f"Plot saved to {output_file}")

    # Also save the data as CSV
    csv_file = os.path.splitext(output_file)[0] + ".csv"
    with open(csv_file, 'w') as f:
        f.write("Current (A),Voltage (V),Power (W),Resistance (Ohm)\n")
        for i in range(len(currents)):
            f.write(f"{currents[i]:.5f},{voltages[i]:.5f},{powers[i]:.5f},{resistances[i]:.5f}\n")
    print(f"Data saved to {csv_file}")

    # Display the plot
    plt.show()

except Exception as e:
    print(f"Error during current sweep: {e}")
    # Attempt to turn off the load in case of error
    try:
        # First set current back to 0
        load.setCIcurrent(0.0, True)
        print("Current set back to 0.0A")

        load.turnInputOFF(True)
        print("Load input turned OFF due to error.")
    except Exception as turn_off_error:
        print(f"Failed to turn off load properly: {turn_off_error}")

finally:
    # Close the socket
    load.closeSocket()
    print("Connection closed.")
