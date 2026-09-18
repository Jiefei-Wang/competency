#pip install git+https://github.com/Jiefei-Wang/extract_inspector.git
#pip install git+https://github.com/anegarza/extract_inspector.git
#pip install --upgrade git+https://github.com/anegarza/extract_inspector.git

import os

import numpy as np
import pandas as pd

from extract_inspector.inspect import Corpus, Inspector, inspector_web

def convert_arrays_to_lists(df: pd.DataFrame) -> pd.DataFrame:
    """Feather list columns load as ndarray cells; inspector expects scalar/list values."""
    clean = df.copy()
    for col in clean.columns:
        if clean[col].map(lambda value: isinstance(value, np.ndarray)).any():
            clean[col] = clean[col].map(
                lambda value: value.tolist() if isinstance(value, np.ndarray) else value
            )
    return clean

#def inject_block_sections(text: str) -> str:
    """Replicates the block section injection logic from the LLM runner."""
    if not isinstance(text, str):
        return text
        
    lines = text.splitlines()
    new_lines = []
    block_num = 1
    for j, line in enumerate(lines):
        if j % 50 == 0:
            new_lines.append(f"block section {block_num}")
            block_num += 1
        new_lines.append(line)
    return "\n".join(new_lines)

note = pd.read_feather("output/pdf_md_ocr.feather")
#note["text"] = note["text"].apply(inject_block_sections)

df = pd.read_feather("output/task2/extraction.feather")

print(df.dtypes)

# find the numpy columns
numpy_cols = [col for col in df.columns if df[col].dtype == 'object' and df[col].apply(lambda x: isinstance(x, np.ndarray)).any()]

note_clean = note.rename(columns={"id": "text_id"})
df_clean = convert_arrays_to_lists(df.rename(columns={"note_id": "text_id"}))

# personalized columns 
supporting_text_cols = [col for col in df_clean.columns if col.endswith("supporting_text")]
shown_cols = [col for col in df_clean.columns 
              if col != "text_id" 
              and not col.endswith("supporting_text") 
              and "confidence" not in col]

corpus = Corpus(
    texts=note_clean,
    text_id_col="text_id",
    text_col="text",
    text_title="Note {text_id}",
)
inspector = Inspector(
    tag_name="task2_extraction",
    entities=df_clean,
    text_id_col="text_id",
    entity_title="Extraction {item_id}",
    shown_cols=shown_cols, #changed to only necessary columns
    highlight_cols=supporting_text_cols,
)

inspector_web(
    corpus,
    inspector,
    #filter_cols=["contain_competence_result"],
    host="127.0.0.1",
    port=5001,
    debug=False,
    open_browser=True,
)



