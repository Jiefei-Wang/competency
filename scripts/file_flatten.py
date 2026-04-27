import argparse
import os
import re
import shutil
import sys
from typing import Dict, Iterable, List, Tuple


ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
SKIP_SUFFIX = ":zone.identifier"
NON_PERSON_KEYWORDS = {
    "document",
    "documents",
    "template",
    "templates",
    "unknown",
    "corrupted",
    "docs",
    "scanned",
    "psych",
    "cds",
    "folder",
}


def normalize_for_compare(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def tokenize_name(value: str) -> Tuple[str, ...]:
    tokens = re.findall(r"[A-Za-z]+", value)
    return tuple(token.lower() for token in tokens if token)


def is_person_folder(folder_name: str) -> bool:
    lowered = folder_name.lower()
    if any(keyword in lowered for keyword in NON_PERSON_KEYWORDS):
        return False
    if any(ch.isdigit() for ch in folder_name):
        return False
    if "." in folder_name and folder_name.lower().endswith(".pdf"):
        folder_name = folder_name[:-4]
        lowered = folder_name.lower()
    if "," in folder_name:
        return True
    words = [word for word in re.split(r"\s+", folder_name.strip()) if word]
    return len(words) >= 2


def file_name_contains_person(file_stem: str, folder_name: str) -> bool:
    folder_tokens = tokenize_name(folder_name)
    if not folder_tokens:
        return False
    file_tokens = set(tokenize_name(file_stem))
    return all(token in file_tokens for token in folder_tokens)


def safe_name(value: str) -> str:
    cleaned = value.replace(os.sep, "_")
    if os.altsep:
        cleaned = cleaned.replace(os.altsep, "_")
    cleaned = cleaned.replace(":", "-")
    cleaned = cleaned.translate({ord(ch): "_" for ch in '<>"/\\|?*'})
    return cleaned.rstrip(" .")


def build_output_name(file_name: str, folder_name: str) -> str:
    stem, ext = os.path.splitext(file_name)
    if is_person_folder(folder_name) and not file_name_contains_person(
        stem, folder_name
    ):
        combined = f"{folder_name} - {file_name}"
        return safe_name(combined)
    return safe_name(file_name)


class ProgressBar:
    def __init__(self, total: int, label: str) -> None:
        self.total = max(total, 1)
        self.label = label
        self.current = 0
        self.width = 30

    def update(self, increment: int = 1) -> None:
        self.current += increment
        ratio = min(self.current / self.total, 1.0)
        filled = int(self.width * ratio)
        bar = "#" * filled + "-" * (self.width - filled)
        percent = int(ratio * 100)
        sys.stdout.write(
            f"\r{self.label}: [{bar}] {percent}% ({self.current}/{self.total})"
        )
        sys.stdout.flush()

    def finish(self) -> None:
        sys.stdout.write("\n")
        sys.stdout.flush()


def count_candidates(data_dir: str) -> int:
    count = 0
    for dirpath, _, filenames in os.walk(data_dir):
        for filename in filenames:
            if filename.lower().endswith(SKIP_SUFFIX):
                continue
            _, ext = os.path.splitext(filename)
            if ext.lower() not in ALLOWED_EXTENSIONS:
                continue
            count += 1
    return count


def iter_candidate_files(data_dir: str, total: int) -> Iterable[Tuple[str, str]]:
    progress = ProgressBar(total, "Scanning files")
    for dirpath, _, filenames in os.walk(data_dir):
        for filename in filenames:
            if filename.lower().endswith(SKIP_SUFFIX):
                continue
            _, ext = os.path.splitext(filename)
            if ext.lower() not in ALLOWED_EXTENSIONS:
                continue
            progress.update()
            yield dirpath, filename
    progress.finish()


def count_trailing_copies(value: str) -> int:
    if not re.search(r"\s*\(\d+\)$", value):
        return 0
    trimmed = value
    count = 0
    while True:
        new_trimmed = re.sub(r"\s*\(\d+\)$", "", trimmed)
        if new_trimmed == trimmed:
            return count
        trimmed = new_trimmed
        count += 1


def is_simpler_name(left: str, right: str) -> bool:
    left_count = count_trailing_copies(left)
    right_count = count_trailing_copies(right)
    if left_count != right_count:
        return left_count < right_count
    if len(left) != len(right):
        return len(left) < len(right)
    return left < right


def canonical_stem(stem: str) -> str:
    return re.sub(r"(\s*\(\d+\))+$", "", stem).strip()


def files_are_equal(path_left: str, path_right: str) -> bool:
    if os.path.getsize(path_left) != os.path.getsize(path_right):
        return False
    chunk_size = 1024 * 1024
    with open(path_left, "rb") as left, open(path_right, "rb") as right:
        while True:
            left_chunk = left.read(chunk_size)
            right_chunk = right.read(chunk_size)
            if left_chunk != right_chunk:
                return False
            if not left_chunk:
                return True


def list_output_files(output_dir: str) -> List[Dict[str, str]]:
    files: List[Dict[str, str]] = []
    for name in os.listdir(output_dir):
        path = os.path.join(output_dir, name)
        if not os.path.isfile(path):
            continue
        stem, ext = os.path.splitext(name)
        files.append(
            {
                "path": path,
                "name": name,
                "stem": stem,
                "ext": ext.lower(),
            }
        )
    return files


def remove_pdf_when_word_exists(output_dir: str) -> int:
    files = list_output_files(output_dir)
    stems_with_word = {
        file["stem"].lower() for file in files if file["ext"] in {".doc", ".docx"}
    }
    progress = ProgressBar(len(files), "Removing pdf duplicates")
    removed = 0
    for file in files:
        if file["ext"] == ".pdf" and file["stem"].lower() in stems_with_word:
            os.remove(file["path"])
            removed += 1
        progress.update()
    progress.finish()
    return removed


def remove_exact_duplicates(output_dir: str) -> int:
    files = list_output_files(output_dir)
    grouped: Dict[Tuple[str, str], List[Dict[str, str]]] = {}
    for file in files:
        canonical = canonical_stem(file["stem"]).lower()
        grouped.setdefault((canonical, file["ext"]), []).append(file)

    total = sum(len(group) for group in grouped.values())
    progress = ProgressBar(total, "Removing exact copies")
    removed = 0
    for group in grouped.values():
        kept: List[Dict[str, str]] = []
        for candidate in group:
            replaced = False
            for index, existing in enumerate(kept):
                if files_are_equal(candidate["path"], existing["path"]):
                    if is_simpler_name(candidate["name"], existing["name"]):
                        os.remove(existing["path"])
                        kept[index] = candidate
                    else:
                        os.remove(candidate["path"])
                    removed += 1
                    replaced = True
                    break
            if not replaced:
                kept.append(candidate)
            progress.update()
    progress.finish()
    return removed


def clear_output_dir(output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    entries = [os.path.join(output_dir, name) for name in os.listdir(output_dir)]
    progress = ProgressBar(len(entries), "Clearing output/raw")
    for entry in entries:
        if os.path.isdir(entry):
            shutil.rmtree(entry)
        else:
            os.remove(entry)
        progress.update()
    progress.finish()


def ensure_unique_path(output_dir: str, file_name: str) -> str:
    candidate = os.path.join(output_dir, file_name)
    if not os.path.exists(candidate):
        return candidate
    stem, ext = os.path.splitext(file_name)
    counter = 1
    while True:
        alt_name = f"{stem} ({counter}){ext}"
        candidate = os.path.join(output_dir, alt_name)
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def flatten_files(
    data_dir: str, output_dir: str
) -> Tuple[int, int, int, int, int, int]:
    os.makedirs(output_dir, exist_ok=True)
    total_candidates = count_candidates(data_dir)
    candidates: List[Dict[str, str]] = []

    for dirpath, filename in iter_candidate_files(data_dir, total_candidates):
        folder_name = os.path.basename(dirpath)
        output_name = build_output_name(filename, folder_name)
        output_stem, ext = os.path.splitext(output_name)
        candidates.append(
            {
                "source_path": os.path.join(dirpath, filename),
                "output_name": output_name,
                "output_stem": output_stem,
                "ext": ext.lower(),
            }
        )

    progress = ProgressBar(len(candidates), "Filtering pdf vs doc/docx")
    stems_with_word = {
        item["output_stem"].lower()
        for item in candidates
        if item["ext"] in {".doc", ".docx"}
    }
    filtered: List[Dict[str, str]] = []
    for candidate in candidates:
        if (
            candidate["ext"] == ".pdf"
            and candidate["output_stem"].lower() in stems_with_word
        ):
            progress.update()
            continue
        filtered.append(candidate)
        progress.update()
    progress.finish()

    grouped: Dict[Tuple[str, str], List[Dict[str, str]]] = {}
    for candidate in filtered:
        canonical = canonical_stem(candidate["output_stem"]).lower()
        key = (canonical, candidate["ext"])
        grouped.setdefault(key, []).append(candidate)

    progress = ProgressBar(len(filtered), "Removing exact duplicates")
    deduped: List[Dict[str, str]] = []
    duplicates_removed = 0
    for group in grouped.values():
        kept: List[Dict[str, str]] = []
        for candidate in group:
            replaced = False
            for index, existing in enumerate(kept):
                if files_are_equal(candidate["source_path"], existing["source_path"]):
                    if is_simpler_name(
                        candidate["output_name"], existing["output_name"]
                    ):
                        kept[index] = candidate
                    duplicates_removed += 1
                    replaced = True
                    break
            if not replaced:
                kept.append(candidate)
            progress.update()
        deduped.extend(kept)
    progress.finish()

    progress = ProgressBar(len(deduped), "Copying files")
    copied = 0
    skipped = 0
    for candidate in deduped:
        destination = ensure_unique_path(output_dir, candidate["output_name"])
        try:
            shutil.copy2(candidate["source_path"], destination)
            copied += 1
        except OSError:
            skipped += 1
        progress.update()
    progress.finish()
    cleanup_pdf_removed = remove_pdf_when_word_exists(output_dir)
    cleanup_duplicates_removed = remove_exact_duplicates(output_dir)
    return (
        copied,
        skipped,
        duplicates_removed,
        len(candidates) - len(filtered),
        cleanup_pdf_removed,
        cleanup_duplicates_removed,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Flatten pdf/doc/docx from data into output/raw.",
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Root data directory to search (default: data)",
    )
    parser.add_argument(
        "--output-dir",
        default=os.path.join("output", "raw"),
        help="Output directory for flattened files (default: output/raw)",
    )
    parser.add_argument(
        "--cleanup-only",
        action="store_true",
        help="Only clean output/raw duplicates without copying new files",
    )
    args = parser.parse_args()

    data_dir = os.path.abspath(args.data_dir)
    output_dir = os.path.abspath(args.output_dir)

    if args.cleanup_only:
        if not os.path.isdir(output_dir):
            raise SystemExit(f"Output directory not found: {output_dir}")
        cleanup_pdf_removed = remove_pdf_when_word_exists(output_dir)
        cleanup_duplicates_removed = remove_exact_duplicates(output_dir)
        print(
            f"Removed {cleanup_pdf_removed} pdf files from output/raw due to doc/docx."
        )
        print(f"Removed {cleanup_duplicates_removed} duplicate copies in output/raw.")
        return

    clear_output_dir(output_dir)

    (
        copied,
        skipped,
        duplicates_removed,
        pdf_skipped,
        cleanup_pdf_removed,
        cleanup_duplicates_removed,
    ) = flatten_files(data_dir, output_dir)
    print(f"Copied {copied} files to {output_dir}.")
    if pdf_skipped:
        print(f"Skipped {pdf_skipped} pdf files because doc/docx exists.")
    if duplicates_removed:
        print(f"Removed {duplicates_removed} exact duplicate copies.")
    if cleanup_pdf_removed:
        print(
            f"Removed {cleanup_pdf_removed} pdf files from output/raw due to doc/docx."
        )
    if cleanup_duplicates_removed:
        print(f"Removed {cleanup_duplicates_removed} duplicate copies in output/raw.")
    if skipped:
        print(f"Skipped {skipped} files due to copy errors.")


if __name__ == "__main__":
    main()
