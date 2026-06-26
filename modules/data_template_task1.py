from typing import Literal
from pydantic import BaseModel, ConfigDict
from datetime import date

class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BaseData(StrictModel):
    value: str | None
    supporting_text: str | None
    confidence: Literal["high", "medium", "low"]


class DateData(StrictModel):
    value: date | None
    supporting_text: str | None
    confidence: Literal["high", "medium", "low"]
   
    
class CompetencyReportExtraction(StrictModel):
    is_competence_to_stand_trial: bool
    header: str | None
    author: BaseData | None
    cause_number: BaseData | None
    date_of_report: DateData | None
    date_of_examination: DateData | None
    block_section_start: int | None
    block_section_end: int | None
