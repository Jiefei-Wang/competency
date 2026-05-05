
# pip install git+https://github.com/Jiefei-Wang/extract_inspector.git
import os

import numpy as np
import pandas as pd

from extract_inspector.inspect import inspect_extractions



def convert_arrays_to_lists(df: pd.DataFrame) -> pd.DataFrame:
    """Feather list columns load as ndarray cells; inspector expects scalar/list values."""
    clean = df.copy()
    for col in clean.columns:
        if clean[col].map(lambda value: isinstance(value, np.ndarray)).any():
            clean[col] = clean[col].map(
                lambda value: value.tolist() if isinstance(value, np.ndarray) else value
            )
    return clean


note = pd.read_feather("output/pdf_md_ocr.feather")
df = pd.read_feather("output/competence_extraction.feather")

print(df.dtypes)

# find the numpy columns
numpy_cols = [col for col in df.columns if df[col].dtype == 'object' and df[col].apply(lambda x: isinstance(x, np.ndarray)).any()]
df.current_charges_value.iloc[0]

note_clean = note.rename(columns={"id": "text_id"})
df_clean = convert_arrays_to_lists(df.rename(columns={"note_id": "text_id"}))

# get all columns ends with supporting_text
supporting_text_cols = [col for col in df_clean.columns if col.endswith("supporting_text")]

inspect_extractions(
    note_clean,
    df_clean,
    text_col="text",
    highlight_col=supporting_text_cols
)

