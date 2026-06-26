from typing import Any, Iterator, Tuple
from pydantic import ValidationError
from scripts.llm_output_parser import parse_json
from modules.data_template_task2 import SocioeconomicFamilyExtraction

def walk_data(data: Any, path: str = "") -> Iterator[Tuple[str, str, dict]]:
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


def validate_socioeconomic_family_task(
    task: Any,
) -> tuple[bool, list[str], dict[str, Any]]:
    if task is None:
        return False, ["Validation failed: task is missing."], {}
        
    ok, reasons, parsed_data = validate_socioeconomic_family_text(
        getattr(task, "output", None)
    )
    
    if not ok:
        return False, reasons, parsed_data
        
    note_text = getattr(task, "original", None)
    if not isinstance(note_text, str):
        return (
            False,
            ["Validation failed: task.original is missing or not a string."],
            parsed_data,
        )
        
    span_issues = validate_text_spans(parsed_data, note_text)
    if span_issues:
        return False, span_issues, parsed_data
        
    return True, [], parsed_data


def validate_socioeconomic_family_text(
    text: Any,
) -> tuple[bool, list[str], dict[str, Any]]:
    if not isinstance(text, str):
        return (
            False,
            ["Validation failed: model output must be a string."],
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
    return validate_socioeconomic_family_payload(payload)


def validate_socioeconomic_family_payload(
    payload: Any,
) -> tuple[bool, list[str], dict[str, Any]]:
    parsed_data = payload if isinstance(payload, dict) else {}
    
    try:
        parsed = SocioeconomicFamilyExtraction.model_validate(
            payload,
            strict=False,
        )
    except ValidationError as exc:
        return False, _format_pydantic_errors(exc), parsed_data 
        
    parsed_data = parsed.model_dump()

    value_issues = validate_field_values(parsed_data)
    if value_issues:
        return False, value_issues, parsed_data    
        
    return True, [], parsed_data


def validate_field_values(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for path, _, item in walk_data(payload):
        value = item.get("value")
        if value is not None:
            if isinstance(value, str) and not value.strip():
                issues.append(f"Field `{path}.value` must not be empty.")
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