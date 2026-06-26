import re
from typing import Any


BLOCK_MARKER_PATTERN = re.compile(r"^block section (\d+)$")


def insert_block_num(notes: list[str], n: int = 50) -> list[str]:
    if n < 1:
        raise ValueError("n must be >= 1.")

    blocked_notes: list[str] = []
    for note in notes:
        lines = str(note).splitlines()
        new_lines: list[str] = []
        block_num = 1

        for idx, line in enumerate(lines):
            if idx % n == 0:
                new_lines.append(f"block section {block_num}")
                block_num += 1
            new_lines.append(line)

        blocked_notes.append("\n".join(new_lines))

    return blocked_notes


def get_block_content(note: str, start_idx: Any, end_idx: Any) -> str | None:
    start = _to_block_index(start_idx)
    end = _to_block_index(end_idx)
    if start is None or end is None or start < 1 or end < start:
        return None

    lines = str(note).splitlines()
    start_line = _find_marker_line(lines, start)
    if start_line is None:
        return None

    next_line = _find_marker_line(lines, end + 1)
    selected_lines = lines[start_line:next_line] if next_line is not None else lines[start_line:]
    content_lines = [
        line for line in selected_lines if BLOCK_MARKER_PATTERN.fullmatch(line.strip()) is None
    ]
    return "\n".join(content_lines).strip()


def _to_block_index(value: Any) -> int | None:
    if value is None:
        return None

    try:
        if value != value:
            return None
        numeric = float(value)
    except (TypeError, ValueError):
        return None

    if not numeric.is_integer():
        return None

    return int(numeric)


def _find_marker_line(lines: list[str], block_idx: int) -> int | None:
    marker = f"block section {block_idx}"
    for idx, line in enumerate(lines):
        if line.strip() == marker:
            return idx
    return None
