#!/usr/bin/env python3
"""
Script to regenerate CSV files for a specified date range.
This will delete existing CSV files and regenerate them with the fixed deduplication logic.

Usage: python regenerate_csvs.py <start_date> <end_date>
Date format: YYYY-MM-DD

If start_date and end_date are the same, only that single day will be processed.
"""

import os
import subprocess
import sys
from datetime import datetime, timedelta

def parse_date(date_str):
    """Parse a date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD")

def regenerate_csvs(start_date, end_date):
    """Regenerate CSV files for the specified date range."""
    
    # Output directory structure
    output_dir = os.path.join('output', 'csv', 'daily')
    
    print(f"Regenerating CSV files from {start_date} to {end_date}")
    print(f"Output directory: {output_dir}")
    
    # Counter for tracking progress
    total_days = (end_date - start_date).days + 1
    current_day = 0
    
    # Iterate through each date
    current_date = start_date
    while current_date <= end_date:
        current_day += 1
        date_str = current_date.strftime("%Y-%m-%d")
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        
        # Build the CSV file path
        csv_path = os.path.join(output_dir, year, month, f"{date_str}.csv")
        
        print(f"\n[{current_day}/{total_days}] Processing {date_str}...")
        
        # Delete existing CSV file if it exists
        if os.path.exists(csv_path):
            try:
                os.remove(csv_path)
                print(f"  Deleted existing file: {csv_path}")
            except Exception as e:
                print(f"  Warning: Could not delete {csv_path}: {e}")
        
        # Run the export_to_csv.py script for this date
        try:
            result = subprocess.run([
                sys.executable, 'export_to_csv.py', date_str
            ], capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                print(f"  ✓ Successfully generated CSV for {date_str}")
                if result.stdout.strip():
                    print(f"    {result.stdout.strip()}")
            else:
                print(f"  ✗ Failed to generate CSV for {date_str}")
                if result.stderr.strip():
                    print(f"    Error: {result.stderr.strip()}")
                if result.stdout.strip():
                    print(f"    Output: {result.stdout.strip()}")
        
        except Exception as e:
            print(f"  ✗ Exception while processing {date_str}: {e}")
        
        # Move to next day
        current_date += timedelta(days=1)
    
    print(f"\nCompleted processing {total_days} days from {start_date} to {end_date}")
    print("All CSV files have been regenerated with the fixed deduplication logic.")

if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python regenerate_csvs.py <start_date> <end_date>")
        print("Date format: YYYY-MM-DD")
        print("Example: python regenerate_csvs.py 2025-04-01 2025-04-15")
        print("For a single day, use the same date for both arguments")
        sys.exit(1)
    
    try:
        start_date = parse_date(sys.argv[1])
        end_date = parse_date(sys.argv[2])
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Validate date range
    if start_date > end_date:
        print("Error: Start date cannot be after end date")
        sys.exit(1)
    
    # Confirm before running
    if start_date == end_date:
        print(f"This script will regenerate CSV file for {start_date}")
    else:
        days_count = (end_date - start_date).days + 1
        print(f"This script will regenerate CSV files for {days_count} days from {start_date} to {end_date}")
    
    print("Actions:")
    print("1. Delete existing CSV files for the specified date range")
    print("2. Regenerate them using the fixed export_to_csv.py script")
    print("3. This may take several minutes depending on the date range")
    
    response = input("\nDo you want to proceed? (y/N): ").strip().lower()
    if response == 'y' or response == 'yes':
        regenerate_csvs(start_date, end_date)
    else:
        print("Operation cancelled.") 