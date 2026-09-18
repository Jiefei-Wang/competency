# Combine all task without supporting text and confidence columns into one CSV for review
import os

import numpy as np
import pandas as pd

def convert_arrays_to_lists(df: pd.DataFrame) -> pd.DataFrame:
    """Feather list columns load as ndarray cells; inspector expects scalar/list values."""
    clean = df.copy()
    for col in clean.columns:
        if clean[col].map(lambda value: isinstance(value, np.ndarray)).any():
            clean[col] = clean[col].map(
                lambda value: value.tolist() if isinstance(value, np.ndarray) else value
            )
    return clean

df1 = pd.read_feather("output/task1/extraction.feather")
df2 = pd.read_feather("output/task2/extraction.feather")
df3 = pd.read_feather("output/task3/extraction.feather")

df1 = df1.rename(columns={"note_id": "text_id"})
df2 = df2.rename(columns={"note_id": "text_id"})
df3 = df3.rename(columns={"note_id": "text_id"})

merged_df = df1.merge(df2, on="text_id", how="outer").merge(df3, on="text_id", how="outer")

# normalize arrays
df_clean = convert_arrays_to_lists(merged_df)

print(merged_df.dtypes)

# Remove supporting_text and confidence columns
cols_to_remove = [col for col in df_clean.columns if col.endswith("supporting_text") or col.endswith("confidence")]
df_clean = df_clean.drop(columns=cols_to_remove)

print(df_clean.head())
    
# Remove rows where competence to stand trial is FALSE
df_clean = df_clean[df_clean["is_competence_to_stand_trial"] == True]

# Remove columns block section
cols_to_remove = [col for col in df_clean.columns if col.startswith("block_")]

# Save the combined DataFrame to a CSV file
output_dir = "output/combined_tasks"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df_clean.to_csv(f"{output_dir}/combined_extraction_review.csv", index=False)

# Keep only the columns that from "Galveston" county for variable "court_county_value" for Jasper review
df_galveston = df_clean[df_clean["court_county_value"] == "Galveston"]

df_galveston.to_csv(f"{output_dir}/galveston_extraction_review.csv", index=False)

