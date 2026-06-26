# For all files in output/pdf_md_ocr, read them as text and save to a feather file with three columns: id, name, and text
import pandas as pd
from pathlib import Path
from tqdm import tqdm
md_path = "output/pdf_md"
md_files = list(Path(md_path).glob("*.md"))
all_text = []
for md_file in tqdm(md_files):
    text = md_file.read_text(encoding="utf-8")
    all_text.append(text)
df = pd.DataFrame({"id": [i for i in range(len(md_files))], "name": [md_file.stem for md_file in md_files], "text": all_text})
df.to_feather("output/pdf_md_ocr.feather")