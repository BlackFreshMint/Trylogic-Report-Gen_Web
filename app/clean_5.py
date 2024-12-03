import os
import pandas as pd
from windowtest import get_selected_file

def clean_csv(input_path, output_path, plantilla_path):
    # Clean the path (strip curly braces or quotes if needed)
    input_path = input_path.strip('{}').strip('"')

    # Print the path to check if it's correct
    print(f"Input file path: {input_path}")

    # Ensure the file path is absolute (in case the current working directory is not correct)
    input_path = os.path.abspath(input_path)

    # Load the input CSV
    try:
        ref_df = pd.read_csv(input_path, header=None, skip_blank_lines=False, low_memory=False)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    plantilla_df = pd.read_csv(plantilla_path, header=None)

    # Remove rows containing unwanted text (e.g., headers, dashes)
    ref_df = ref_df.loc[~ref_df[0].astype(str).str.contains('Chronolgical Listing', na=False)]
    ref_df = ref_df.loc[~ref_df[0].astype(str).str.contains('-----', na=False)]
    ref_df = ref_df.reset_index(drop=True)

    # Add 'unit' column dynamically
    if 'Actual' in ref_df.iloc[0].values:
        actual_col_index = ref_df.iloc[0].tolist().index('Actual')
        ref_df.insert(actual_col_index + 1, 'unit', '')  # Add empty 'unit' column after 'Actual'

    num_columns = plantilla_df.shape[1]
    cleaned_rows = []

    for index, row in ref_df.iterrows():
        row = row.dropna().tolist()
        if 'm3' in row:
            row.remove('m3')
            row = row + [''] * (num_columns - len(row))
        if len(row) > num_columns:
            row = row[:num_columns]
        else:
            row = row + [''] * (num_columns - len(row))
        cleaned_rows.append(row)

    cleaned_df = pd.DataFrame(cleaned_rows, columns=range(num_columns))

    for _, template_row in plantilla_df.iterrows():
        if template_row.astype(str).str.contains('-----').any():
            cleaned_df.loc[len(cleaned_df)] = ['-----'] + [''] * (num_columns - 1)
        elif template_row.isnull().all():
            cleaned_df.loc[len(cleaned_df)] = [''] * num_columns

    cleaned_df.to_csv(output_path, index=False, header=False)
    print(f"Cleaned file saved to: {output_path}")

if __name__ == "__main__":
    plantilla_path = "plantilla_csv.csv"  # Path to the template CSV
    output_path = "cleaned_data_exam.csv"  # Path to save the cleaned file

    print("Drag and drop your file into the window.")
    input_file = get_selected_file()  # Use drag-and-drop functionality

    if input_file:
        try:
            clean_csv(input_file, output_path, plantilla_path)
        except Exception as e:
            print(f"Error processing file: {e}")
    else:
        print("No file was selected. Please try again.")
