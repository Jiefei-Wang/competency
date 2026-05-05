from typing import Literal
from pydantic import BaseModel, ConfigDict
from datetime import date

class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BaseData(StrictModel):
    value: str | list[str] | None
    supporting_text: str | None
    confidence: Literal["high", "medium", "low"]

class DateData(StrictModel):
    date_text: str | None
    date_precision: Literal["day", "month", "year"] | None
    date_day: int | None
    date_month: int | None
    date_year: int | None
    supporting_text: str | None
    confidence: Literal["high", "medium", "low"]


class CompetencyReportData(StrictModel):
    contain_competence_result: Literal["yes", "no"]

    header: BaseData | None
    author: BaseData | None
    date_of_examination: date | None
    date_of_report: date | None
    cause_number: BaseData | None
    evaluee_name: BaseData | None
    evaluee_dob: DateData | None
    reason_for_evaluation: BaseData | None
    current_charges: BaseData | None
    birth_place: BaseData | None
    family: BaseData | None
    childhood_development: BaseData | None
    education: BaseData | None
    employment: BaseData | None
    legal_history: BaseData | None
    military_history: BaseData | None
    psychiatric_history: BaseData | None
    substance_use: BaseData | None
    medical_history: BaseData | None
    mental_status_examination: BaseData | None
    areas_of_competency: BaseData | None
    opinion: BaseData | None
    recommendations: BaseData | None