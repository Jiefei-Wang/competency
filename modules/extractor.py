from collections.abc import Iterable
from types import UnionType
from typing import Any, Union, get_args, get_origin

import pandas as pd
from llm_output_parser import parse_json
from pydantic import BaseModel


SchemaTree = dict[str, "SchemaTree | None"]


def results_to_dataframe(
    results: Iterable[Any],
    data_template: type[BaseModel],
) -> pd.DataFrame:
    schema_tree = _build_schema_tree(data_template)
    expected_columns = _schema_columns(schema_tree)
    rows = []

    for idx, result in enumerate(results):
        note_id = getattr(result, "note_id", None)
        output, parse_warning = _parse_output(getattr(result, "output", None))

        if parse_warning:
            print(f"Warning: result {idx} note_id={note_id}: {parse_warning}")

        row = {"note_id": note_id}
        row.update({column: None for column in expected_columns})

        if output:
            row.update(_flatten_expected(output, schema_tree))
            extras = _flatten_unrecognized(output, schema_tree)
            for path, value in extras.items():
                row[_path_to_column(path)] = value
                print(
                    f"Warning: result {idx} note_id={note_id}: unrecognized field `{path}`."
                )

        rows.append(row)

    return pd.DataFrame(rows, columns=_ordered_columns(rows, expected_columns))


def _parse_output(output: Any) -> tuple[dict[str, Any], str | None]:
    if isinstance(output, dict):
        return output, None
    if isinstance(output, str):
        try:
            parsed = parse_json(output, strict=False)
        except Exception as exc:
            return {}, f"output could not be parsed as JSON. Parser error: {exc}"
        if isinstance(parsed, dict):
            return parsed, None
        return {}, "parsed output is not a JSON object."
    if output is None:
        return {}, "output is missing."
    return {}, f"output has unsupported type {type(output).__name__}."


def _build_schema_tree(data_template: type[BaseModel]) -> SchemaTree:
    tree: SchemaTree = {}

    for field_name, field_info in data_template.model_fields.items():
        nested_model = _nested_model_type(field_info.annotation)
        if nested_model is None:
            tree[field_name] = None
        else:
            tree[field_name] = _build_schema_tree(nested_model)

    return tree


def _nested_model_type(annotation: Any) -> type[BaseModel] | None:
    for item in _unwrap_union(annotation):
        if isinstance(item, type) and issubclass(item, BaseModel):
            return item
    return None


def _unwrap_union(annotation: Any) -> tuple[Any, ...]:
    origin = get_origin(annotation)
    if origin in (UnionType, Union):
        return get_args(annotation)
    return (annotation,)


def _schema_columns(schema_tree: SchemaTree, prefix: str = "") -> list[str]:
    columns: list[str] = []

    for field_name, child_schema in schema_tree.items():
        column = f"{prefix}_{field_name}" if prefix else field_name
        if child_schema is None:
            columns.append(column)
        else:
            columns.extend(_schema_columns(child_schema, column))

    return columns


def _flatten_expected(
    output: dict[str, Any],
    schema_tree: SchemaTree,
    prefix: str = "",
) -> dict[str, Any]:
    flat: dict[str, Any] = {}

    for field_name, child_schema in schema_tree.items():
        column = f"{prefix}_{field_name}" if prefix else field_name
        value = output.get(field_name)

        if child_schema is None:
            flat[column] = value
        elif isinstance(value, dict):
            flat.update(_flatten_expected(value, child_schema, column))
        else:
            for child_column in _schema_columns(child_schema, column):
                flat[child_column] = None

    return flat


def _flatten_unrecognized(
    output: dict[str, Any],
    schema_tree: SchemaTree,
    prefix: str = "",
) -> dict[str, Any]:
    flat: dict[str, Any] = {}

    for field_name, value in output.items():
        child_schema = schema_tree.get(field_name, "__missing__")
        path = f"{prefix}.{field_name}" if prefix else field_name

        if child_schema == "__missing__":
            flat.update(_flatten_any(value, path))
        elif isinstance(child_schema, dict) and isinstance(value, dict):
            flat.update(_flatten_unrecognized(value, child_schema, path))

    return flat


def _flatten_any(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {path: value}

    flat: dict[str, Any] = {}
    for key, item in value.items():
        flat.update(_flatten_any(item, f"{path}.{key}"))
    return flat


def _path_to_column(path: str) -> str:
    return path.replace(".", "_")


def _ordered_columns(rows: list[dict[str, Any]], expected_columns: list[str]) -> list[str]:
    columns = ["note_id", *expected_columns]
    seen = set(columns)

    for row in rows:
        for column in row:
            if column not in seen:
                columns.append(column)
                seen.add(column)

    return columns
