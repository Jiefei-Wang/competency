from typing import Any

from llm_output_parser import parse_json
from pydantic import ValidationError

from modules.data_template import CompetencyReportData


BASE_DATA_FIELDS = (
    "header",
    "author",
    "cause_number",
    "evaluee_name",
    "reason_for_evaluation",
    "current_charges",
    "birth_place",
    "family",
    "childhood_development",
    "education",
    "employment",
    "legal_history",
    "military_history",
    "psychiatric_history",
    "substance_use",
    "medical_history",
    "mental_status_examination",
    "areas_of_competency",
    "opinion",
    "recommendations",
)

DATE_DATA_FIELDS = (
    "date_of_examination",
    "date_of_report",
    "evaluee_dob",
)

LIST_VALUE_FIELDS = (
    "current_charges",
    "employment",
    "legal_history",
    "psychiatric_history",
    "substance_use",
    "medical_history",
)

ALL_EXTRACTION_FIELDS = BASE_DATA_FIELDS + DATE_DATA_FIELDS


def validate_competency_report_task(task: Any) -> tuple[bool, list[str], dict[str, Any]]:
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
                "Validation failed: task.original is missing or not a string, so supporting text spans cannot be checked."
            ],
            parsed_data,
        )

    span_issues = validate_text_spans(parsed_data, note_text)
    if span_issues:
        return False, span_issues, parsed_data

    return True, [], parsed_data


def validate_competency_report_text(text: Any) -> tuple[bool, list[str], dict[str, Any]]:
    if not isinstance(text, str):
        return (
            False,
            [
                "Validation failed: the model output must be plain text before it can be parsed as JSON."
            ],
            {},
        )

    try:
        payload = parse_json(text, strict=False)
    except Exception as exc:
        return (
            False,
            [
                "Validation failed: the model output could not be parsed as JSON.",
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
        parsed = CompetencyReportData.model_validate(payload, strict=True)
    except ValidationError as exc:
        return False, _format_pydantic_errors(exc), parsed_data

    parsed_data = parsed.model_dump()

    no_result_issues = validate_no_result_fields(parsed_data)
    if no_result_issues:
        return False, no_result_issues, parsed_data

    date_issues = validate_date_precision(parsed_data)
    if date_issues:
        return False, date_issues, parsed_data

    value_issues = validate_field_values(parsed_data)
    if value_issues:
        return False, value_issues, parsed_data

    return True, [], parsed_data


def validate_no_result_fields(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    if payload.get("contain_competence_result") != "no":
        return issues

    for field in ALL_EXTRACTION_FIELDS:
        if payload.get(field) is not None:
            issues.append(
                f"Field `{field}` must be null when `contain_competence_result` is `no`."
            )

    return issues


def validate_date_precision(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    for field in DATE_DATA_FIELDS:
        item = payload.get(field)
        if item is None:
            continue

        precision = item.get("date_precision")
        year = item.get("date_year")
        month = item.get("date_month")
        day = item.get("date_day")

        if year is not None and not 1000 <= year <= 9999:
            issues.append(
                f"Field `{field}.date_year` must be a 4-digit year when available."
            )
        if month is not None and not 1 <= month <= 12:
            issues.append(f"Field `{field}.date_month` must be between 1 and 12.")
        if day is not None and not 1 <= day <= 31:
            issues.append(f"Field `{field}.date_day` must be between 1 and 31.")

        if year is None and (month is not None or day is not None):
            issues.append(
                f"Field `{field}.date_year` must be set when date_month or date_day is set."
            )
        if month is None and day is not None:
            issues.append(
                f"Field `{field}.date_month` must be set when date_day is set."
            )

        if precision is None:
            if year is not None or month is not None or day is not None:
                issues.append(
                    f"Field `{field}.date_precision` must be set when any date part is set."
                )
        elif precision == "year":
            if year is None:
                issues.append(
                    f"Field `{field}.date_year` must be set when date_precision is `year`."
                )
            if month is not None:
                issues.append(
                    f"Field `{field}.date_month` must be null when date_precision is `year`."
                )
            if day is not None:
                issues.append(
                    f"Field `{field}.date_day` must be null when date_precision is `year`."
                )
        elif precision == "month":
            if year is None:
                issues.append(
                    f"Field `{field}.date_year` must be set when date_precision is `month`."
                )
            if month is None:
                issues.append(
                    f"Field `{field}.date_month` must be set when date_precision is `month`."
                )
            if day is not None:
                issues.append(
                    f"Field `{field}.date_day` must be null when date_precision is `month`."
                )
        elif precision == "day":
            if year is None:
                issues.append(
                    f"Field `{field}.date_year` must be set when date_precision is `day`."
                )
            if month is None:
                issues.append(
                    f"Field `{field}.date_month` must be set when date_precision is `day`."
                )
            if day is None:
                issues.append(
                    f"Field `{field}.date_day` must be set when date_precision is `day`."
                )

    return issues


def validate_field_values(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    for field in BASE_DATA_FIELDS:
        item = payload.get(field)
        if item is None:
            continue

        value = item.get("value")
        if value is None:
            issues.append(
                f"Field `{field}` should be null instead of an object when no value is available."
            )

        if field in LIST_VALUE_FIELDS and value is not None and not isinstance(value, list):
            issues.append(f"Field `{field}.value` must be a list of strings.")

        if isinstance(value, list):
            for idx, entry in enumerate(value):
                if not isinstance(entry, str) or not entry.strip():
                    issues.append(
                        f"Field `{field}.value[{idx}]` must be a non-empty string."
                    )
        elif isinstance(value, str) and not value.strip():
            issues.append(f"Field `{field}.value` must not be an empty string.")

    for field in DATE_DATA_FIELDS:
        item = payload.get(field)
        if item is None:
            continue

        date_text = item.get("date_text")
        precision = item.get("date_precision")
        year = item.get("date_year")
        month = item.get("date_month")
        day = item.get("date_day")
        if (
            date_text is None
            and precision is None
            and year is None
            and month is None
            and day is None
        ):
            issues.append(
                f"Field `{field}` should be null instead of an object when no date is available."
            )

        if isinstance(date_text, str) and not date_text.strip():
            issues.append(f"Field `{field}.date_text` must not be an empty string.")

    return issues


def validate_text_spans(payload: dict[str, Any], note_text: str) -> list[str]:
    issues: list[str] = []

    for field in BASE_DATA_FIELDS:
        item = payload.get(field)
        if item is None:
            continue

        supporting_text = item.get("supporting_text")
        if isinstance(supporting_text, str) and supporting_text:
            if supporting_text not in note_text:
                issues.append(
                    f"Field `{field}.supporting_text` was not found in the input note text. Copy an exact supporting span from the note."
                )

    for field in DATE_DATA_FIELDS:
        item = payload.get(field)
        if item is None:
            continue

        supporting_text = item.get("supporting_text")
        date_text = item.get("date_text")

        if isinstance(supporting_text, str) and supporting_text:
            if supporting_text not in note_text:
                issues.append(
                    f"Field `{field}.supporting_text` was not found in the input note text. Copy an exact supporting span from the note."
                )

        if isinstance(date_text, str) and date_text:
            if date_text not in note_text:
                issues.append(
                    f"Field `{field}.date_text` was not found in the input note text. Copy the date exactly as it appears in the note, or use null when no date is stated."
                )

    return issues


def _format_pydantic_errors(exc: ValidationError) -> list[str]:
    reasons = ["Validation failed: the JSON does not match CompetencyReportData."]
    for error in exc.errors():
        location = ".".join(str(part) for part in error["loc"]) or "payload"
        reasons.append(f"Field `{location}`: {error['msg']}")
    return reasons


# Backward-compatible aliases for callers that still use the old validator names.
validate_cancer_stage_task = validate_competency_report_task
validate_cancer_stage_text = validate_competency_report_text
validate_cancer_stage_payload = validate_competency_report_payload
