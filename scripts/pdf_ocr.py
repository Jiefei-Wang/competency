from pathlib import Path
import subprocess

input_dir = Path("output/raw")
output_dir = Path("output/pdf_ocr")

output_dir.mkdir(parents=True, exist_ok=True)

pdf_files = sorted(input_dir.glob("*.pdf"))

# Exclude files that already exist in output/pdf_ocr
files_to_process = [
    pdf_file
    for pdf_file in pdf_files
    if not (output_dir / pdf_file.name).exists()
]

total = len(files_to_process)
failed = 0

for i, pdf_file in enumerate(files_to_process, start=1):
    output_file = output_dir / pdf_file.name

    print(f"[{i}/{total}] Processing: {pdf_file}")

    result = subprocess.run(
        [
            "ocrmypdf",
            "--skip-text",
            "--optimize", "3",
            str(pdf_file),
            str(output_file),
        ],
        check=False,
    )

    if result.returncode != 0:
        failed += 1
        print(f"[{i}/{total}] Failed: {pdf_file}")

print(f"Done! Processed {total} file(s), {failed} failed.")