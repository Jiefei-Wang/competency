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
    value: bool | None
    supporting_text: str | None
    confidence: Literal["high", "medium", "low"] 
    
class OperationData(StrictModel):
    operator: Literal["=", ">="] | None
    value: int | None
    supporting_text: str | None
    confidence: Literal["high", "medium", "low"]

class HistoryLegalCompetence(StrictModel):
    #relashionships history
    current_marital_status: BaseData 
    total_marriages: IntData 
    total_divorces: IntData 
    number_of_children: IntData 
    
    #psychiatric history
    current_psychiatric_diagnosis: BaseData
    current_psychiatric_medications: BaseData 
    number_of_psychiatric_hospitalizations: OperationData
    history_of_suicide_thoughts: BooleanData
    history_of_self_harm_behavior: BooleanData
    number_of_suicide_attempts: OperationData
    history_of_violence: BooleanData
    
    #substance use history
    substance_use_disorder_diagnosis: BaseData
    type_of_substance_used: BaseData 
    age_of_first_use: IntData
    most_recent_use: IntData

    #past medical history
    prior_psychiatric_diagnosis: BaseData 
    prior_diagnosis: BaseData
    current_medications: BaseData
    
    #legal history
    number_of_arrests: IntData
    number_of_incarcerations: IntData
    total_time_incarcerated: IntData
    #incarceration_durations: IntData SAME AS THE TOTAL DURATION IN MONTHS? 
    history_of_prior_charges: BooleanData
    number_of_prior_charges: IntData
    history_of_prior_convictions: BooleanData
    number_of_prior_convictions: IntData
    #charges: BaseData ALREADY PROCESSED IN TASK 2 AS CURRENT_CHARGES = RAW TEXT
    number_of_competency_exams: IntData
    number_of_times_found_incompetent: IntData
    age_at_first_crime: IntData
    depressive_symptoms: BooleanData
    manic_symptoms: BooleanData
    anxiety_symptoms: BooleanData
    PTSD_symptoms: BooleanData
    psychotic_symptoms: BooleanData
    suicidal_ideation_behavior: BooleanData
    agitated_behavior: BooleanData
    violence_agression: BooleanData
    
    #competence recommendations
    factual_understanding: BooleanData
    rational_understanding: BooleanData
    ability_to_assist_in_own_defense: BooleanData
    competent_to_stand_trial: BooleanData
    restorable_if_incompetent: BooleanData
