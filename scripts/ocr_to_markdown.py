from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import pymupdf4llm

src_dir = Path("output/raw")
dst_dir = Path("output/pdf_md")
nworker = 4


def convert_pdf(pdf_path: str) -> tuple[str, str]:
    pdf_path = Path(pdf_path)
    md = pymupdf4llm.to_markdown(str(pdf_path), use_ocr=True)
    return pdf_path.stem, md


def main() -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(src_dir.glob("*.pdf"))

    # exclude already converted files at the beginning
    pdf_files = [
        pdf_path
        for pdf_path in pdf_files
        if not (dst_dir / f"{pdf_path.stem}.md").exists()
    ]

    if not pdf_files:
        print("No PDFs left to convert.")
        return

    with ProcessPoolExecutor(max_workers=min(len(pdf_files), nworker)) as executor:
        futures = {
            executor.submit(convert_pdf, str(pdf_path)): pdf_path for pdf_path in pdf_files
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc="Converting PDFs"):
            pdf_path = futures[future]
            try:
                stem, md = future.result()
            except Exception as exc:
                print(f"Failed: {pdf_path} ({exc})")
                continue
            (dst_dir / f"{stem}.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
