import os
import pandas as pd

def clean_csv(input_path, output_path, plantilla_path):
    input_path = input_path.strip('{}').strip('"')
    input_path = os.path.abspath(input_path)

    print(f"Input file path: {input_path}")
    print(f"Plantilla CSV path: {plantilla_path}")

    if not os.path.exists(plantilla_path):
        raise FileNotFoundError(f"Template file 'plantilla_csv.csv' does not exist at {plantilla_path}")

    try:
        ref_df = pd.read_csv(input_path, header=None, skip_blank_lines=False, low_memory=False)
    except Exception as e:
        raise Exception(f"Error reading input file: {e}")

    try:
        plantilla_df = pd.read_csv(plantilla_path, header=None)
    except Exception as e:
        raise Exception(f"Error reading template file: {e}")

    # Cleaning logic (same as provided earlier)
    ref_df = ref_df.loc[~ref_df[0].astype(str).str.contains('Chronolgical Listing', na=False)]
    ref_df = ref_df.loc[~ref_df[0].astype(str).str.contains('-----', na=False)]
    ref_df = ref_df.reset_index(drop=True)

    if 'Actual' in ref_df.iloc[0].values:
        actual_col_index = ref_df.iloc[0].tolist().index('Actual')
        ref_df.insert(actual_col_index + 1, 'unit', '')

    num_columns = plantilla_df.shape[1]
    cleaned_rows = []

    for _, row in ref_df.iterrows():
        row = row.dropna().tolist()
        if 'm3' in row:
            row.remove('m3')
            row += [''] * (num_columns - len(row))
        if len(row) > num_columns:
            row = row[:num_columns]
        else:
            row += [''] * (num_columns - len(row))
        cleaned_rows.append(row)

    cleaned_df = pd.DataFrame(cleaned_rows, columns=range(num_columns))

    for _, template_row in plantilla_df.iterrows():
        if template_row.astype(str).str.contains('-----').any():
            cleaned_df.loc[len(cleaned_df)] = ['-----'] + [''] * (num_columns - 1)
        elif template_row.isnull().all():
            cleaned_df.loc[len(cleaned_df)] = [''] * num_columns

    cleaned_df.to_csv(output_path, index=False, header=False)
    print(f"Cleaned file saved to: {output_path}")
