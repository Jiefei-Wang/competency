from collections.abc import Iterator
from typing import Any

from llm_output_parser import parse_json
from pydantic import BaseModel, ValidationError

from modules.data_template import CompetencyReportData


def validate_task(
    task: Any,
    data_template: type[BaseModel],
) -> tuple[bool, list[str], dict[str, Any]]:
    if task is None:
        return False, ["Validation failed: task is missing."], {}

    output = getattr(task, "output", None)
    if isinstance(output, str):
        ok, reasons, parsed_data = validate_text(output, data_template)
    else:
        ok, reasons, parsed_data = validate_payload(output, data_template)
    if not ok and not parsed_data:
        return False, reasons, parsed_data

    supporting_paths = list(_find_supporting_text_fields(parsed_data))
    if not supporting_paths:
        return ok, reasons, parsed_data

    note_text = getattr(task, "original", None)
    if not isinstance(note_text, str):
        reasons.append(
            "Validation failed: task.original is missing or not a string, so supporting text spans cannot be checked."
        )
        return (
            False,
            reasons,
            parsed_data,
        )

    span_issues = validate_text_spans(parsed_data, note_text)
    reasons.extend(span_issues)
    if reasons:
        return False, reasons, parsed_data

    return True, [], parsed_data


def validate_text(
    text: Any,
    data_template: type[BaseModel],
) -> tuple[bool, list[str], dict[str, Any]]:
    if not isinstance(text, str):
        return False, ["Validation failed: model output must be a string."], {}

    try:
        payload = parse_json(text, strict=False)
    except Exception as exc:
        return (
            False,
            [
                "Validation failed: model output could not be parsed as JSON.",
                f"Parser error: {exc}",
            ],
            {},
        )

    return validate_payload(payload, data_template)


def validate_payload(
    payload: Any,
    data_template: type[BaseModel],
) -> tuple[bool, list[str], dict[str, Any]]:
    parsed_data = payload if isinstance(payload, dict) else {}

    try:
        parsed = data_template.model_validate(payload, strict=False)
    except AttributeError:
        return (
            False,
            ["Validation failed: data_template must be a Pydantic model class."],
            parsed_data,
        )
    except ValidationError as exc:
        return False, _format_pydantic_errors(exc, data_template), parsed_data

    parsed_data = parsed.model_dump()
    value_issues = validate_field_values(parsed_data)
    if value_issues:
        return False, value_issues, parsed_data

    return True, [], parsed_data


def validate_field_values(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    for path, value in _walk_values(payload):
        if isinstance(value, str) and not value.strip():
            issues.append(f"Field `{path}` must not be empty.")
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                if isinstance(item, str) and not item.strip():
                    issues.append(f"Field `{path}[{idx}]` must not be empty.")

    return issues


def validate_text_spans(payload: dict[str, Any], note_text: str) -> list[str]:
    issues: list[str] = []
    normalized_note = normalize_text(note_text)

    for path, supporting_text in _find_supporting_text_fields(payload):
        if not isinstance(supporting_text, str) or not supporting_text.strip():
            continue

        if normalize_text(supporting_text) not in normalized_note:
            issues.append(f"Field `{path}` was not found in source note.")

    return issues


def normalize_text(text: str) -> str:
    return "".join(text.split())


def _walk_values(data: Any, path: str = "") -> Iterator[tuple[str, Any]]:
    if isinstance(data, dict):
        for key, value in data.items():
            child_path = f"{path}.{key}" if path else str(key)
            if key == "value":
                yield child_path, value
            yield from _walk_values(value, child_path)
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            child_path = f"{path}[{idx}]" if path else f"[{idx}]"
            yield from _walk_values(item, child_path)


def _find_supporting_text_fields(data: Any, path: str = "") -> Iterator[tuple[str, Any]]:
    if isinstance(data, dict):
        for key, value in data.items():
            child_path = f"{path}.{key}" if path else str(key)
            if key == "supporting_text" or key.endswith("_supporting_text"):
                yield child_path, value
            yield from _find_supporting_text_fields(value, child_path)
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            child_path = f"{path}[{idx}]" if path else f"[{idx}]"
            yield from _find_supporting_text_fields(item, child_path)


def _format_pydantic_errors(
    exc: ValidationError,
    data_template: type[BaseModel],
) -> list[str]:
    template_name = getattr(data_template, "__name__", "data template")
    reasons = [f"Validation failed: JSON does not match {template_name}."]
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"]) or "payload"
        reasons.append(f"Field `{location}`: {error['msg']}")
    return reasons


def validate_competency_report_task(task: Any) -> tuple[bool, list[str], dict[str, Any]]:
    return validate_task(task, CompetencyReportData)


def validate_competency_report_text(text: Any) -> tuple[bool, list[str], dict[str, Any]]:
    return validate_text(text, CompetencyReportData)


def validate_competency_report_payload(
    payload: Any,
) -> tuple[bool, list[str], dict[str, Any]]:
    return validate_payload(payload, CompetencyReportData)


# Backward-compatible aliases for callers that still use the old validator names.
validate_cancer_stage_task = validate_competency_report_task
validate_cancer_stage_text = validate_competency_report_text
validate_cancer_stage_payload = validate_competency_report_payload
