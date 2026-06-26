import os

# tune these to your VRAM
os.environ["RECOGNITION_BATCH_SIZE"] = "384"
os.environ["DETECTOR_BATCH_SIZE"] = "18"
os.environ["LAYOUT_BATCH_SIZE"] = "32"
os.environ["TABLE_REC_BATCH_SIZE"] = "48"


from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered


artifacts = create_model_dict()
converter = PdfConverter(artifact_dict=artifacts)



file_name = 'output/raw/YUQUIMPO CHRISTOPHER 09-10-18.pdf'
rendered = converter(file_name)
text, _, images = text_from_rendered(rendered)

file_md = file_name.split("/")[-1].split(".")[0]
with open(f"output/{file_md}.md", "w") as file:
    file.write(text)




from marker.converters.ocr import OCRConverter
from marker.models import create_model_dict

converter_ocr = OCRConverter(
    artifact_dict=create_model_dict(),
)
rendered2 = converter_ocr("data/Forensic Psychiatry Lab Scanned/Harris, Cherrod/Harris, Cherrod (1990-08-07).pdf")

rendered2





file_name = 'output/raw/YUQUIMPO CHRISTOPHER 09-10-18.pdf'

from pdf2image import convert_from_path

# Replace 'input_file.pdf' with the path to your PDF file
pdf_file = 'input_file.pdf'
pages = convert_from_path(pdf_file)







from pathlib import Path
import subprocess
import pymupdf4llm

src = 'data/Forensic Psychiatry Lab Scanned/Harris, Cherrod/Harris, Cherrod (1990-08-07).pdf'
ocr_pdf = "output/input_ocr.pdf"
out_md = "output/output.md"

# 1) OCR the scanned PDF
subprocess.run(
    ["ocrmypdf", "--skip-text", src, ocr_pdf],
    check=True
)

# 2) Convert OCR'd PDF to Markdown
import pymupdf4llm
path = "output/pdf_ocr/3.pdf"
md = pymupdf4llm.to_markdown(path)




with open(out_md, "w") as file:
    file.write(md)



from markitdown import MarkItDown
# from openai import OpenAI

path = "output/pdf_ocr/3.pdf"
md = MarkItDown()
result = md.convert(path)
print(result.text_content)
