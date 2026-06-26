from collections.abc import Iterable
from typing import Any
import pandas as pd
from llm_output_parser import parse_json

def results_to_dataframe(
    results: Iterable[Any],
) -> pd.DataFrame:
    rows = []

    for result in results:
        output = _parse_output(getattr(result, "output", None))
        
        # If the LLM failed to output anything, skip it
        if not output:
            continue

        row = {"note_id": getattr(result, "note_id", None)}
        row.update(_flatten_dict(output))
        rows.append(row)

    return pd.DataFrame(rows)


def _parse_output(output: Any) -> dict[str, Any]:
    if isinstance(output, dict):
        return output
    if isinstance(output, str):
        parsed = parse_json(output, strict=False)
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _flatten_dict(data: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    flat = {}
    for key, value in data.items():
        column = f"{prefix}_{key}" if prefix else key
        
        # Because DateData, IntData, BooleanData, and BaseData all share the 
        # same shape (value, supporting_text, confidence), we recursively flatten.
        if isinstance(value, dict):
            flat.update(_flatten_dict(value, column))
        else:
            flat[column] = value

    return flat