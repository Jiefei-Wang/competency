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


class IntData(StrictModel):
    value: int | None
    supporting_text: str | None
    confidence: Literal["high", "medium", "low"]
    
    
class BooleanData(StrictModel):
    value: bool
    supporting_text: str | None
    confidence: Literal["high", "medium", "low"] 
    
   
    
class CompetencyReportExtraction(StrictModel):
    is_competence_to_stand_trial: bool
    header: BaseData
    examiner: BaseData
    cause_number: BaseData
    date_of_report: DateData
    date_of_examination: DateData
    court_county: BaseData
    court_number: IntData
    evaluation_location: BaseData
    facility_type: BaseData
    currently_incarcerated: BooleanData
    examiner_qualifications: BaseData
    block_section_start: IntData
    block_section_end: IntData
