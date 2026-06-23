import pandas as pd
import os

def split_csv_by_days(file_path, x_days, y_days):
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Load the CSV file
    print(f"Reading {file_path}...")
    df = pd.read_csv(file_path)

    # Convert the datetime column to actual datetime objects
    # Assuming 'datetime' is the column name based on your file structure
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Get unique dates in chronological order
    unique_dates = sorted(df['datetime'].dt.date.unique())
    total_days = len(unique_dates)
    
    print(f"Found {total_days} unique days in the file.")

    # Validate inputs
    if x_days + y_days > total_days:
        print(f"Warning: The sum of x ({x_days}) and y ({y_days}) is greater than the total available days ({total_days}).")
        print("Adjusting to use available data...")
    
    # Identify the dates for each part
    part1_dates = unique_dates[:x_days]
    part2_dates = unique_dates[x_days : x_days + y_days]

    # Filter the data
    part1_df = df[df['datetime'].dt.date.isin(part1_dates)]
    part2_df = df[df['datetime'].dt.date.isin(part2_dates)]

    # Save to new CSV files
    base_name = os.path.splitext(file_path)[0]
    part1_filename = f"{base_name}_part1_{x_days}days.csv"
    part2_filename = f"{base_name}_part2_{y_days}days.csv"

    part1_df.to_csv(part1_filename, index=False)
    part2_df.to_csv(part2_filename, index=False)

    print(f"Successfully created:")
    print(f" - {part1_filename} ({len(part1_df)} rows, {len(part1_dates)} days)")
    print(f" - {part2_filename} ({len(part2_df)} rows, {len(part2_dates)} days)")

if __name__ == "__main__":
    # Get user inputs
    csv_file = input("Enter the CSV filename (e.g., AKBA_1min_RTH_40days.csv): ")
    try:
        x = int(input("Enter number of days for the first part (x): "))
        y = int(input("Enter number of days for the second part (y): "))
        
        split_csv_by_days(csv_file, x, y)
    except ValueError:
        print("Please enter valid numbers for x and y.")