# pip install extract_inspector 
from collections.abc import Iterable
from typing import Any

import pandas as pd
from llm_output_parser import parse_json

def results_to_dataframe(
    results: Iterable[Any],
    keep_flag: str = "is_competence_to_stand_trial",
    keep_value: bool = True,
) -> pd.DataFrame:
    rows = []

    for result in results:
        output = _parse_output(getattr(result, "output", None))
        if output.get(keep_flag) != keep_value:
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
        if isinstance(value, dict):
            flat.update(_flatten_dict(value, column))
        else:
            flat[column] = value

    return flat


def _is_date_data(value: Any) -> bool:
    if not isinstance(value, dict):
        return False

    date_keys = {
        "date_text",
        "date_precision",
        "date_day",
        "date_month",
        "date_year",
    }
    return date_keys.issubset(value)


def _normalized_date(value: dict[str, Any]) -> str | None:
    year = value.get("date_year")
    month = value.get("date_month")
    day = value.get("date_day")
    precision = value.get("date_precision")

    if precision == "year" and year is not None:
        return f"{year:04d}"
    if precision == "month" and year is not None and month is not None:
        return f"{year:04d}-{month:02d}"
    if precision == "day" and year is not None and month is not None and day is not None:
        return f"{year:04d}-{month:02d}-{day:02d}"

    return None
