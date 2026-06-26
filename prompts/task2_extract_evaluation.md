Extract the socioeconomic, family, developmental delay, and social history information from the Competence to Stand Trial evaluation reports.

Your output structure must strictly follow the schema template below:
{schema}

Below are the definitions for the data elements in the schema. For each object, you must provide the value, the verbatim supporting text, and a confidence score.

- evaluee_name:
  * value: The full name of the defendant/evaluee being examined. 
  * supporting_text: Verbatim text snippet stating the name. It may most easily be located after the phrase "Name of Defendant", "Defendant", or "Identifying Information". 

- evaluee_date_of_birth:
  * value: The date of birth of the evaluee, formatted strictly as YYYY-MM-DD.
  * supporting_text: Verbatim phrase containing the date of birth (e.g., "DOB: 01/23/1990"). This will be most likely found after the phrase “Evaluation Date:” or “Date of Evaluation:”.

- evaluee_age:
  * value: The age of the evaluee at the time of the evaluation. Must be a number.
  * supporting_text: Verbatim text snippet indicating the evaluee's age (e.g., "is a 26 year old male"). Most reports will say the age of the patient, stating the number right before the phrase “year old”. 

- evaluee_sex:
  * value: The biological sex or gender of the evaluee (e.g., "Male", "Female").
  * supporting_text: Verbatim text snippet confirming the sex.

- evaluee_race:
  * value: The stated race, ethnicity, or descent/ancestry of the evaluee (e.g., "White", "Caucasian", "Hispanic", "Mixed", "African American").
  * supporting_text: Verbatim text snippet confirming the race.

- current_charges:
  * value: The specific legal offenses or crimes the evaluee is currently charged with (e.g., Evaluee Name is X years old sex who is charged with "Aggravated Assault", "Theft", "Capital Murder", "Retaliation").  
  * supporting_text: Verbatim text snippet confirming the current charges.

- family_history_mental_illness:
  * value: Set to true ONLY IF the text indicates ANY family history of psychiatric or mental illness. Set to false ONLY IF the text explicitly states the evaluee denied a family history of mental illness.
  * supporting_text: Verbatim text proving the history.

- family_history_addiction:
  * value: Set to true ONLY IF the text indicates ANY family members with a history of addiction. Set to false ONLY IF ANY family history of substance abuse or addiction is explicitly denied.
  * supporting_text: Verbatim text proving the history.

- family_history_suicide:
  * value: Set to true ONLY IF the text indicates a family history of suicide. Suicide includes only completed suicides, not unsuccessful suicide attempts. Set to false ONLY IF a family history of suicide is explicitly denied.
  * supporting_text: Verbatim text proving the history.

- birthplace:
  * value: The city in which the evaluee was born. If possible, include the county, state, and country.
  * supporting_text: Verbatim text snippet confirming the birthplace. 

- number_of_siblings:
  * value: The total number of siblings, living or dead, the evaluee has/had. Include stepsiblings. Must be a number.
  * supporting_text: Verbatim text snippet confirming the number of siblings.

- development_delays:
  * value: Set to true ONLY IF the text mentions childhood developmental delays. These include physical delays, such as delayed gross motor development, intellectual delays, such as learning disabilities, and social delays, such as those seen in autism. Set to false  ONLY IF childhood developmental delays are explicitly denied.
  * supporting_text: Verbatim text proving the history. 

- parents_married:
  * value: Set to true ONLY IF the text indicates the evaluee's parents were married to each other. Set to false ONLY IF explicitly denied or stated otherwise (e.g., "parents never married").
  * supporting_text: Verbatim text proving the marital status. 

- parents_divorced:
  * value: Set to true ONLY IF the text indicates the evaluee's parents legally separated or divorced. Set to false ONLY IF evaluee's parents legally separated or divorced is explicitly denied.
  * supporting_text: Verbatim text proving the divorce or separation. 

- parent_death:
  * value: Set to true ONLY IF the text indicates one or both of the evaluee's parents died. Set to false ONLY IF explicitly denied (e.g., "both parents are living").
  * supporting_text: Verbatim text proving the death of a parent.

- parent_death_age:
  * value: The age of the evaluee when their parent died, or the age of the parent at the time of death. Must be a number. 
  * supporting_text: Verbatim text snippet indicating the age related to the parent's death.

- history_physical_abuse:
  * value: Set to true ONLY IF the text indicates a history of physical abuse against the evaluee. This includes beatings, whippings, caustic injuries, or other acts of violence that cause physical harm. Set to false ONLY IF physical abuse against the evaluee is explicitly denied.
  * supporting_text: Verbatim text proving the history. 

- history_sexual_abuse:
  * value: Set to true ONLY IF the text indicates a history of sexual abuse against the evaluee. This includes being the victim of sexual assault/rape, molestation, production of child sexual abuse material (CSAM), pressure to engage in sexual activity, and other forms of sexual abuse. Set to false ONLY IF history of sexual abuse against the evaluee is explicitly denied.
  * supporting_text: Verbatim text proving the history. 

- history_emotional_abuse:
  * value: Set to true ONLY IF the text indicates a history of emotional or psychological abuse against the evaluee. This includes bullying, frequent insulting, gaslighting, belittling, and threatening. Set to false ONLY IF history of emotional or psychological abuse against the evaluee is explicitly denied.
  * supporting_text: Verbatim text proving the history. 

- history_physical_neglect:
  * value: Set to true ONLY IF the text indicates a history of physical neglect (e.g., lack of supervision, medical neglect, abandonment). Set to false ONLY IF a history of physical neglect is explicitly denied.
  * supporting_text: Verbatim text proving the history. 

- history_emotional_neglect:
  * value: Set to true ONLY IF the text indicates a history of emotional neglect. This includes a parent, guardian, close friend, or partner being dismissive of the patient’s feelings, being purposely emotionally distant, failing to provide adequate social support, or punishing appropriate expressions of emotion. Set to false ONLY IF a history of emotional neglect is explicitly denied.
  * supporting_text: Verbatim text proving the history. 

- unstable_housing:
  * value: Set to true ONLY IF the text indicates a history of homelessness, transient living, or unstable housing. Housing insecurity in this context refers to a state of being in which someone does not have consistent access to safe shelter. This includes homelessness, couch surfing, and homeless shelter use. Set to false ONLY IF explicitly denied.
  * supporting_text: Verbatim text proving the history.

- history_food_insecurity:
  * value: Set to true ONLY IF the text indicates a history of food insecurity, starvation, or lacking adequate meals. This includes any time that the patient did not have access to sufficient amounts of food, or they only had access to food of inadequate quality. Set to false ONLY IF explicitly denied.
  * supporting_text: Verbatim text proving the history.

- current_household_status:
  * value: The evaluee's current living arrangement or who they reside with (e.g., "lives alone", "lives with mother", "homeless shelter"). If evaluee states that they have stable or consistent housing, then output “Domicile”. If the evaluee states that they are homeless, couch surfing, utilizing a homeless shelter, living in their non-RV vehicle, or any other statement that makes clear they do not have stable housing, then output “Homeless”.  If the evaluee's housing situation is unclear orunstated, then output “Unknown”.
  * supporting_text: Verbatim text snippet confirming the household status. 

- highest_level_of_education:
  * value: The highest grade completed or degree earned by the evaluee (e.g., "10th grade", "High School Diploma", "GED"). If the evaluee completed elementary school, but not middle school, output "Elementary". If evaluee completed middle school, but not high school, then output “Middle School”. If evaluee completed high school, but did not pursue college, then output “High School”. If evaluee did not complete high school, but later earned a GED, and did not pursue college thereafter, then output “GED”. If evaluee completed some college, but did not achieve a college degree, then “Some College”. If evaluee completed an undergraduate degree at a college, then “College Graduate”. If the evaluee completed graduate-level education, such as a graduate degree, then “Graduate School/Professional Degree”. If not stated or unclear, then “Null”
  * supporting_text: Verbatim text snippet confirming the education level. 

- suspension_from_school:
  * value: Set to true ONLY IF the text indicates the evaluee was ever suspended from school. Set to false ONLY IF evaluee was ever suspended from school is explicitly denied.
  * supporting_text: Verbatim text proving the history. 

- number_of_suspensions:
  * value: The total number of times the evaluee was suspended. Must be a number. If the exact number of times is not stated, make your best estimate based on what is written.
  * supporting_text: Verbatim text snippet confirming the number of suspensions. 

- expulsion_from_school:
  * value: Set to true ONLY IF the text indicates the evaluee was ever expelled from school. Set to false ONLY IF evaluee was ever expelled from school is explicitly denied.
  * supporting_text: Verbatim text proving the history. 

- number_of_expulsions:
  * value: The total number of times the evaluee was expelled. If the exact number of times is not stated, make your best estimate based on what is written. Must be a number.
  * supporting_text: Verbatim text snippet confirming the number of expulsions. 

- behavioral_problems_in_school:
  * value: Set to true ONLY IF the text mentions behavioral issues, disciplinary actions, or acting out in school. This includes verbal reprimands, reported truancy, detention, complaints from teachers, or any other disciplinary measure that does not reach the threshold of suspension or expulsion. Set to false ONLY IF behavioral issues, disciplinary actions, or acting out in school are explicitly denied .
  * supporting_text: Verbatim text proving the history. 

- history_of_bullying:
  * value: Set to true ONLY IF the text indicates the evaluee was a victim of bullying. This includes verbal, physical, and emotional altercations that do not rise to the level of abuse or neglect, especially if the word “bullying” is explicitly used. Set to false ONLY IF evaluee being a victim of bullying is explicitly denied.
  * supporting_text: Verbatim text proving the history. 

- current_employment_status:
  * value: The evaluee's employment status at the time of the evaluation (e.g., "Employed Full-time", "Unemployed", "Receiving Disability"). If the evaluee is unemployed, then output “Unemployed”. If the evaluee has a job for part of the year, such as a summer or holiday job, then output “Seasonal”. If the evaluee has a job, and it is unclear whether the job is part- or full-time, then output “Employed”. If the evaluee has a part-time job, then output “Part-Time”. If the evaluee has a full-time job, then output “Full-Time”. If evaluee is unemployed and receiving social security disability checks, then output "Receiving Disability". Do not include a parent’s job, or the evaluee’s future career plans. 
  * supporting_text: Verbatim text snippet confirming the employment status. This will likely appear near the terms “job”, “employee”, “employer”, or “career”. 

- longest_duration_of_employment:
  * value: Based on a evaluee's stated history of employment state the longest continuous period the evaluee held a single job (e.g., "5 years", "6 months"). This includes any stretch of time not broken up by at least 1 month of unemployment. The output should be the length of the patient’s longest period of employment, rounded to the nearest month. 
  * supporting_text: Verbatim text snippet confirming the duration. Information related to this will often be found in a specific section entitled “Employment Hx”. 

- primary_industry_of_employment:
  * value: The main type of work, trade, or industry the evaluee has worked in (e.g., "Construction", “Healthcare”, "Fast food", “Financial Services”, “Education”, “Military”, "Retail"). If evaluee has been employed in multiple industries, select the one that they have worked for the longest in, or is their primary career. 
  * supporting_text: Verbatim text snippet confirming the industry. This information will most likely be found in the “Employment Hx” section. Some documents include “Employer name” which can be used to determine the industry the patient works in. 


Important Extraction Rules:
- Verbatim Quotes Only: For any field requiring supporting_text, you MUST extract the exact, verbatim text snippet from the document that proves or contains the extracted value.
- Null Values: If a specific piece of information is completely missing from the data elements above, set the entire object to null.
- Confidence Scoring: Set confidence to "high" only if the verbatim text explicitly and unambiguously confirms the value. Set it to "medium" or "low" if there is ambiguity, typos, or if you are inferring the value from messy OCR context.
- Critical Boolean Rule: You must distinguish between "Denied" and "Not Mentioned". If a report explicitly says a history is denied, output false. If the report simply does not talk about it, you MUST output null for both the value and supporting_text.
- Mandatory Output: You MUST always return the requested JSON object. Even if the text contains absolutely no socioeconomic or family history information. Return the complete JSON schema with all missing fields set to null.

- For the sections about family history and developmental history it can often be found under a specific section, either labeled “Marriage/Relationships/Children”, “Personal/Family Hx”, “Family History”, “Family, Personal, Educational, and Social History”, or particularly under the “Reared by” heading. It may also often be found near the terms “Learning d/o", “Developmental”, “Educational Hx”, “Personal”, “Family”, “Social”, “History”, and “Hx”.

Return JSON only. Do NOT wrap the JSON response in markdown code blocks (```json). Now analyze this OCR report excerpt:

{{report}}