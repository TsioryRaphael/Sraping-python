import os
import pandas as pd

# Specify the directory containing CSV files
directory = "./entreprises"

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Read the CSV file
        csv_path = os.path.join(directory, filename)
        df = pd.read_csv(csv_path)
        
        # Create Excel filename by replacing .csv with .xlsx
        excel_filename = os.path.splitext(filename)[0] + ".xlsx"
        excel_path = os.path.join(directory, excel_filename)
        
        # Save to Excel
        df.to_excel(excel_path, index=False)
        print(f"Converted {filename} to {excel_filename}")