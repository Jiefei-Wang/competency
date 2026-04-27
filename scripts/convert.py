import os
from tqdm import tqdm

# tune these to your VRAM
os.environ["RECOGNITION_BATCH_SIZE"] = "384"
os.environ["DETECTOR_BATCH_SIZE"] = "18"
os.environ["LAYOUT_BATCH_SIZE"] = "32"
os.environ["TABLE_REC_BATCH_SIZE"] = "48"


from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from marker.config.parser import ConfigParser

# create output/markdown if not exist
if not os.path.exists("output/markdown"):
    os.makedirs("output/markdown")


config = config={
    
    # "disable_tqdm": True,
        "force_ocr": False,   # critical
        "disable_table_extraction": True,
        "recognition_batch_size": 8,
        "layout_batch_size": 4,
    }

config_parser = ConfigParser(config)

artifacts = create_model_dict()
converter = PdfConverter(artifact_dict=artifacts,
                        config=config)

# list all pdf in output/raw
pdf_files = [f for f in os.listdir("output/raw") if f.endswith(".pdf")]
# list all existing markdown files in output/markdown
md_files = [f for f in os.listdir("output/markdown") if f.endswith(".md")]
# get the pdf files that do not have corresponding markdown files
pdf_files = [f for f in pdf_files if f.split(".")[0] + ".md" not in md_files]

for file_name in tqdm(pdf_files):
    rendered = converter("output/raw/" +file_name)
    text, _, images = text_from_rendered(rendered)
    file_md = file_name.split("/")[-1].split(".")[0]
    with open(f"output/markdown/{file_md}.md", "w") as file:
        file.write(text)