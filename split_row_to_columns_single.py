
import pandas as pd
import os
import re

# Specify the input Excel file (change this to your file's path or name)
input_file = "./entreprises/Entreprise.xlsx" 

# Check if the file exists
if not os.path.exists(input_file):
    print(f"Error: The file '{input_file}' does not exist.")
    exit()

# Load the Excel file
try:
    df = pd.read_excel(input_file)
except Exception as e:
    print(f"Error reading '{input_file}': {e}")
    exit()

# Check if the file is empty
if df.empty:
    print(f"Error: The file '{input_file}' is empty.")
    exit()


# Function to split values, handling multiple commas
def split_values(value):
    if isinstance(value, str) and ',' in value:
        # Split on one or more commas and remove empty strings
        split_vals = [v.strip() for v in re.split(r',+', value) if v.strip()]
        return split_vals if split_vals else [value]
    return [str(value) if pd.notnull(value) else '']  # Handle non-string or NaN

# Process the first row to get new column headers
first_row = df.iloc[0]
print("\nRaw first row:")
print(first_row.tolist())

# Split the first row's values
new_columns = []
for value in first_row:
    split_vals = split_values(value)
    print(f"Value: {value} -> Split: {split_vals}")
    new_columns.extend(split_vals)

print(f"\nNew column headers: {new_columns}")

# Process all rows to split values, including the first row
new_data = []
for index, row in df.iterrows():
    row_values = []
    for value in row:
        row_values.extend(split_values(value))
    print(f"\nRow {index} split values: {row_values}")
    new_data.append(row_values)

# Create a new DataFrame with the split values
# Use the first row's split values as headers, truncate or pad rows to match
max_cols = len(new_columns)
new_df = pd.DataFrame(
    [row + [None] * (max_cols - len(row)) if len(row) < max_cols else row[:max_cols] for row in new_data],
    columns=new_columns
)

# Create output filename by appending "_split" to the original name
output_file = os.path.splitext(input_file)[0] + "_split.xlsx"

# Save the new DataFrame to a new Excel file
try:
    new_df.to_excel(output_file, index=False)
    print(f"\nProcessed '{input_file}' and saved as '{output_file}'")
except Exception as e:
    print(f"Error saving '{output_file}': {e}")
