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
    
class SocioeconomicFamilyExtraction(StrictModel):
    #sociodemographic
    evaluee_name: BaseData
    evaluee_date_of_birth: DateData
    evaluee_age: IntData
    evaluee_sex: BaseData
    evaluee_race: BaseData
    current_charges: BaseData
    offense_type: BaseData
    
    #family history
    family_history_mental_illness: BooleanData
    family_history_addiction: BooleanData
    family_history_suicide: BooleanData
    
    #developmental history
    birthplace: BaseData
    number_of_siblings: OperationData
    development_delays: BooleanData
    special_education: BooleanData
    parents_married: BooleanData
    parents_divorced: BooleanData
    parent_death: BooleanData 
    parent_death_age: BaseData # Age of the evaluee when either parent died. If younger than 18 then "childhood", if 18 or older then "adulthood".
    childhood_parent_death: BooleanData
    history_physical_abuse: BooleanData
    history_sexual_abuse: BooleanData
    history_emotional_abuse: BooleanData
    history_physical_neglect: BooleanData
    history_emotional_neglect: BooleanData
    history_unstable_housing: BooleanData # If the evaluee states that they have stable or consistent housing then “Domicile”, otherwise homeless, couch surfing, homeless shelter, non-RV vehicle then "Homeless".
    history_food_insecurity: BooleanData 
    
    #social history
    current_household_status: BaseData # If evaluee states that they have stable or consistent housing, then output “Domicile”. If the evaluee states that they are homeless, couch surfing, utilizing a homeless shelter, living in their non-RV vehicle, or any other statement that makes clear they do not have stable housing, then output “Homeless”.  If the evaluee's housing situation is unclear orunstated, then output “Unknown”.
    highest_level_of_education: BaseData 
    suspension_from_school: BooleanData
    number_of_suspensions: IntData
    expulsion_from_school: BooleanData 
    number_of_expulsions: IntData
    behavioral_problems_in_school: BooleanData
    academic_problems_in_school: BooleanData
    history_of_bullying: BooleanData | None
    history_of_being_bullied: BooleanData | None
    current_employment_status: BaseData
    longest_duration_of_employment: IntData
    primary_industry_of_employment: BaseData