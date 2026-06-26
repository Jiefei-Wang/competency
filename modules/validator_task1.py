from typing import Any, Iterator, Tuple

from pydantic import ValidationError

from llm_output_parser import parse_json
from modules.data_template_task1 import CompetencyReportExtraction


def walk_data(data: Any, path: str = "") -> Iterator[Tuple[str, str, dict]]:
    """Yields paths and objects for BaseData and DateData schemas."""
    if isinstance(data, dict):
        if "value" in data and "confidence" in data:
            yield path, "ExtractedData", data
        else:
            for k, v in data.items():
                new_path = f"{path}.{k}" if path else k
                yield from walk_data(v, new_path)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            yield from walk_data(item, f"{path}[{i}]")


def validate_competency_report_task(
    task: Any,
) -> tuple[bool, list[str], dict[str, Any]]:
    if task is None:
        return False, ["Validation failed: task is missing."], {}
    ok, reasons, parsed_data = validate_competency_report_text(
        getattr(task, "output", None)
    )
    if not ok:
        return False, reasons, parsed_data
    note_text = getattr(task, "original", None)
    if not isinstance(note_text, str):
        return (
            False,
            [
                "Validation failed: task.original is missing or not a string."
            ],
            parsed_data,
        )
    span_issues = validate_text_spans(parsed_data, note_text)
    if span_issues:
        return False, span_issues, parsed_data
    return True, [], parsed_data


def validate_competency_report_text(
    text: Any,
) -> tuple[bool, list[str], dict[str, Any]]:
    if not isinstance(text, str):
        return (
            False,
            [
                "Validation failed: model output must be a string."
            ],
            {},
        )
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
    return validate_competency_report_payload(payload)

def validate_competency_report_payload(
    payload: Any,
) -> tuple[bool, list[str], dict[str, Any]]:
    parsed_data = payload if isinstance(payload, dict) else {}
    try:
        parsed = CompetencyReportExtraction.model_validate(
            payload,
            strict=False,
        )
    except ValidationError as exc:
        return False, _format_pydantic_errors(exc), parsed_data 
    parsed_data = parsed.model_dump()
    no_result_issues = validate_no_result_fields(parsed_data)
    if no_result_issues:
        return False, no_result_issues, parsed_data    
    value_issues = validate_field_values(parsed_data)
    if value_issues:
        return False, value_issues, parsed_data    
    block_issues = validate_block_ranges(parsed_data)
    if block_issues:
        return False, block_issues, parsed_data
    return True, [], parsed_data

def validate_no_result_fields(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    is_competency = payload.get("is_competence_to_stand_trial")
    
    if is_competency is False:
        # If false, check that root extraction fields are None
        fields_to_check = ['header', 'author', 'cause_number', 'date_of_report', 'date_of_examination', 'block_section_start', 'block_section_end']
        for field in fields_to_check:
            if payload.get(field) is not None:
                issues.append(f"Field `{field}` must be null when `is_competence_to_stand_trial` is false.")
    return issues

def validate_field_values(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for path, _, item in walk_data(payload):
        value = item.get("value")
        if value is not None:
            # Check if the value is an empty string
            if isinstance(value, str) and not value.strip():
                issues.append(f"Field `{path}.value` must not be empty.")
    return issues

def validate_block_ranges(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    start = payload.get("block_section_start")
    end = payload.get("block_section_end")
    
    if start is not None and start < 1:
        issues.append("Field `block_section_start` must be >= 1.")
    if end is not None and end < 1:
        issues.append("Field `block_section_end` must be >= 1.")
    if start is not None and end is not None and start > end:
        issues.append("Field `block_section_start` cannot be greater than `block_section_end`.")
        
    return issues

def normalize_text(text: str) -> str:
    return "".join(text.split())

def validate_text_spans(payload: dict[str, Any], note_text: str) -> list[str]:
    issues: list[str] = []
    norm_note = normalize_text(note_text)
    
    for path, _, item in walk_data(payload):
        supporting_text = item.get("supporting_text")
        if isinstance(supporting_text, str) and supporting_text:
            if normalize_text(supporting_text) not in norm_note:
                issues.append(f"Field `{path}.supporting_text` was not found in source note.")
                
    return issues

def _format_pydantic_errors(exc: ValidationError) -> list[str]:
    reasons = ["Validation failed: JSON does not match schema."]
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"]) or "payload"
        reasons.append(f"Field `{location}`: {error['msg']}")
    return reasons