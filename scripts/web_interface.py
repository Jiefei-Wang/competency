# pip install git+https://github.com/Jiefei-Wang/extract_inspector.git

import os

import numpy as np
import pandas as pd

try:
    from extract_inspector.inspect import inspect_extractions
except ImportError:
    from extract_inspector.inspect import Corpus, Inspector, inspector_web

    def inspect_extractions(texts: pd.DataFrame, entities: pd.DataFrame, text_col: str = "text", highlight_col=None):
        if isinstance(highlight_col, str):
            highlight_col = [highlight_col]
        if highlight_col is None:
            highlight_col = []

        corpus = Corpus(texts=texts, text_id_col="text_id", text_col=text_col)
        inspector = Inspector(
            tag_name="extractions",
            entities=entities,
            text_id_col="text_id",
            shown_cols=[col for col in entities.columns if col != "text_id"],
            highlight_cols=highlight_col,
        )
        inspector_web(corpus, inspector, open_browser=True)



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
df = pd.read_feather("output/extraction_1,2,3.feather")

# normalize arrays
df_clean = convert_arrays_to_lists(df)

print(df_clean.dtypes)

# find the numpy columns
numpy_cols = [col for col in df_clean.columns if df_clean[col].dtype == 'object' and df_clean[col].apply(lambda x: isinstance(x, np.ndarray)).any()]
#df.current_charges_value.iloc[0]

note_clean = note.rename(columns={"id": "text_id"})

# get all columns ends with supporting_text
supporting_text_cols = [col for col in df_clean.columns if col.endswith("supporting_text")]
shown_cols = [col for col in df_clean.columns 
              if col != "text_id" 
              and not col.endswith("supporting_text") 
              and "confidence" not in col]

corpus = Corpus(
    texts=note_clean,
    text_id_col="text_id",
    text_col="text",
    text_title="Note {name}",
)

inspector = Inspector(
    tag_name="task_extraction",
    entities=df_clean,
    text_id_col="text_id",
    entity_title="Extraction {item_id}",
    shown_cols=shown_cols, #changed to only necessary columns
    highlight_cols=supporting_text_cols,
)

inspector_web(
    corpus,
    inspector,
    filter_cols=["contain_competence_result"],
    host="127.0.0.1",
    port=5001,
    debug=False,
    open_browser=True,
)

# Previous Inspector
inspect_extractions(
    note_clean,
    df_clean,
    text_col="name",
    highlight_col=supporting_text_cols
)

