Extract the socioeconomic, family, developmental delay, and social history information from the Competence to Stand Trial evaluation reports.

Your output structure must strictly follow the schema template below:
{schema}

Below are the definitions for the data elements in the schema. For each object, you must provide the value, the verbatim supporting text, and a confidence score.

- evaluee_name:
  * value: The full name of the defendant/evaluee being examined (last name, middle name, and first name). 
  * supporting_text: Verbatim text snippet stating the name. It may most easily be located after the phrase "Name of Defendant", "Defendant", or "Identifying Information". 

- evaluee_date_of_birth:
  * value: The date of birth of the evaluee, formatted strictly as YYYY-MM-DD.
  * supporting_text: Verbatim phrase containing the date of birth. This will be most likely found after the phrase “Evaluation Date:” or “Date of Evaluation:”.

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

- offense_type:
  * value: Classify each offense listed in `current_charges` into one or more of the following categories: "Violent Offenses", "Property Offenses", "Violent Sexual Offenses", "Non-Violent Sexual Offenses", "Drug Offenses", or "Other". Base this classification on the extracted `current_charges`. If all current charges belong to the same category, output that category once. If the current charges belongs to multiple categories, output each applicable category separated by commas.
  * supporting_text: Use the same verbatim supporting text that confirms the `current_charges` used for the classification.

- family_history_mental_illness:
  * value: Set to true ONLY IF the text indicates ANY family history of psychiatric or mental illness. Set to false ONLY IF the text explicitly states the evaluee denied a family history of mental illness.
  * supporting_text: Verbatim text proving the history of family mental illness.

- family_history_addiction:
  * value: Set to true ONLY IF the text indicates ANY family members with a history of addiction. Set to false ONLY IF ANY family history of substance abuse or addiction is explicitly denied.
  * supporting_text: Verbatim text proving the history of family addiction.

- family_history_suicide:
  * value: Set to true ONLY IF the text indicates a family history of suicide. Suicide includes only completed suicides, not unsuccessful suicide attempts. Set to false ONLY IF a family history of suicide is explicitly denied.
  * supporting_text: Verbatim text proving the history of family suicide.

- birthplace:
  * value: The city in which the evaluee was born. If available, include the county, state, and country.
  * supporting_text: Verbatim text snippet confirming the birthplace. 

- number_of_siblings:
  * value: Extract the total number of siblings the evaluee has or had, including biological siblings, half‑siblings, and step‑siblings, living or deceased. Do NOT include: cousins, parents, aunts/uncles, grandparents. If the text gives a specific number, output that integer. If the text says “multiple siblings,” “several siblings,” “siblings” (plural), set "operator": ">=", "value": 2".
  . If an exact count is provided, output the integer. If the record states "multiple siblings," "several siblings," output value as the operator ">=" and the integer 2. 
  * supporting_text: Verbatim snippet confirming the sibling count.

- development_delays:
  * value: Indicates the presence of childhood speech or motor skill delays. Set to true ONLY if the text explicitly reports issues with speaking, language development, or motor skills during childhood. Set to false ONLY if the evaluee explicitly denies a childhood history of speech or motor delays.
  * supporting_text: Verbatim text proving the history of developmental delays.

- special_education:
 * value: Set to true ONLY if the evaluee reports attending, receiving, or requiring special education services or classes during childhood or adolescence. Set to false ONLY if the evaluee explicitly states they did not attend or require special education services or classes.
 * supporting_text: Verbatim text proving special classes attended.

- parents_married:
  * value: Set to true ONLY IF the text indicates the evaluee's parents were married to each other. Set to false ONLY IF explicitly denied or stated otherwise (e.g., "parents never married").
  * supporting_text: Verbatim text proving the marital status. 

- parents_divorced:
  * value: Set to true ONLY IF the text indicates the evaluee's parents legally separated or divorced. Set to false ONLY IF evaluee's parents legally separated or divorced is explicitly denied.
  * supporting_text: Verbatim text proving the divorce or separation. 

- parent_death:
  * value: Set to true ONLY if stated that one or both of the evaluee's parents died. Set to false ONLY if death is explicityly denied or stated that the parent(s) are alive ("both parents are living", "living with my parents and siblings when I got arrested"). 
  * supporting_text: Verbatim text proving the death of a parent.

- parent_death_age: 
  * value: The age of the evaluee when their parent died. If the exact age is not stated but the report differentiates between childhood and adulthood, then we extract the categorical ("childhood", or "adulthood") variable.
  * supporting_text: The verbatim text snippet indicating the evaluee's age or life stage related to the parent's death.

- childhood_parent_death:
  * value: Set to true ONLY if confirmed parental death occurred during childhood (or under 18). Set to false ONLY if parental death occurred during adulthood (or 18, or older).
  * supporting_text: Use the same verbatim text supporting the evaluee's age or life stage at the time of the parent's death.

- history_physical_abuse:
  * value: Set to true ONLY IF the text indicates a history of physical abuse against the evaluee. This includes beatings, whippings, caustic injuries, or other acts of violence that cause physical harm. Set to false ONLY IF physical abuse against the evaluee is explicitly denied.
  * supporting_text: Verbatim text proving the history of physical abuse. 

- history_sexual_abuse:
  * value: Set to true ONLY IF the text indicates a history of sexual abuse against the evaluee. This includes being the victim of sexual assault/rape, molestation, production of child sexual abuse material (CSAM), pressure to engage in sexual activity, and other forms of sexual abuse. Set to false ONLY IF history of sexual abuse against the evaluee is explicitly denied.
  * supporting_text: Verbatim text proving the history or sexual abuse. 

- history_emotional_abuse:
  * value: Set to true ONLY IF the text indicates a history of emotional or psychological abuse against the evaluee. This includes bullying, frequent insulting, gaslighting, belittling, and threatening. Set to false ONLY IF history of emotional or psychological abuse against the evaluee is explicitly denied.
  * supporting_text: Verbatim text proving the history of emotional abuse. 

- history_physical_neglect:
  * value: Set to true ONLY IF the text indicates a history of physical neglect (e.g., lack of supervision, medical neglect, abandonment). Set to false ONLY IF a history of physical neglect is explicitly denied.
  * supporting_text: Verbatim text proving the history os physical neglect. 

- history_emotional_neglect:
  * value: Set to true ONLY IF the text indicates a history of emotional neglect. This includes a parent, guardian, close friend, or partner being dismissive of the patient’s feelings, being purposely emotionally distant, failing to provide adequate social support, or punishing appropriate expressions of emotion. Set to false ONLY IF a history of emotional neglect is explicitly denied.
  * supporting_text: Verbatim text proving the history of emotional neglect. 

- history_unstable_housing:
  * value: Set to true ONLY IF the text indicates a history of homelessness, transient living, or unstable housing. Housing insecurity in this context refers to a state of being in which someone does not have consistent access to safe shelter. This includes homelessness, couch surfing, homeless shelter use, or evaluee living in more than three residences within one year. Set to false ONLY IF explicitly denied.
  * supporting_text: Verbatim text proving the history of unstable housing.

- history_food_insecurity:
  * value: Set to true ONLY IF the text indicates a history of food insecurity, starvation, or lacking adequate meals. This includes any time that the patient did not have access to sufficient amounts of food, or they only had access to food of inadequate quality. Set to false ONLY IF explicitly denied.
  * supporting_text: Verbatim text proving the history of food insecurity.

- current_household_status:
  * value:  The evaluee’s last housing situation prior to arrest. Output "Domicile" when the evaluee describes stable or consistent housing, including: living alone, with parents, grandparents, aunts/uncles, cousins, siblings, partner/spouse,  friends in a stable arrangement, in a family home, or in any residence that is clearly stable and not transient. Any housing with relatives (including extended family) MUST be classified as "Domicile". Output "Homeless" when the evaluee describes unstable housing, including: homeless, couch surfing, homeless shelter, living in a car, living in a tent, living in an RV without hookups, or any statement indicating lack of stable housing. Output "Other" ONLY when the housing is: hotel, motel, nursing home, assisted living, group home, halfway house, transitional housing, rehab facility, any non‑family, or non‑stable institutional setting.
  * supporting_text: Verbatim text snippet confirming the household status.  

- highest_level_of_education:
  * value: The highest level of formal education the evaluee has experienced. If the evaluee completed graduate-level education, such as a graduate degree, then “Graduate School/Professional Degree”. If evaluee completed an undergraduate degree at a college, then “College Graduate”. If the evaluee attended ANY college classes, even briefly, and did NOT complete a degree, you MUST output "Some College". If evaluee completed technical or vocational school, then “Technical/Vocational School”. If evaluee did not complete high school, but later earned a GED, and did not pursue college thereafter, then output “GED”. If evaluee did not pursue college, but completed high school then output “High School”. Do not stop reading at "High School". If the text states the evaluee completed high school/GED, but also mentions they attended ANY college classes or coursework (e.g., "completed some coursework at college") without earning a degree, you MUST output "Some College". If the evaluee did not complete high school, output "Middle School". If the evaluee did not complete middle school, output "Elementary".
  * supporting_text: Verbatim text snippet confirming the education level. 

- suspension_from_school:
  * value: Set to true ONLY IF the text indicates the evaluee was ever suspended from school. Set to false ONLY IF evaluee was ever suspended from school is explicitly denied.
  * supporting_text: Verbatim text proving the history of school suspensions. 

- number_of_suspensions:
  * value: The total number of times the evaluee was suspended. Must be a number. If explicitly stated that evaluee was NEVER suspended, then output "0". If the exact number of times is not stated, make your best estimate based on what is written. If no suspensions mentioned, then empty output " ". 
  * supporting_text: Verbatim text snippet confirming the number of suspensions. 

- expulsion_from_school:
  * value: Set to true ONLY IF the text indicates the evaluee was ever expelled from school. Set to false ONLY IF evaluee was ever expelled from school is explicitly denied.
  * supporting_text: Verbatim text proving the history of school expulsions. 

- number_of_expulsions:
  * value: The total number of times the evaluee was expelled. If mentioned that evaluee was NEVER expelled, then output "0". If the exact number of times is not stated, make your best estimate based on what is written. If no expulsions mentioned, then empty output " ". 
  * supporting_text: Verbatim text snippet confirming the number of expulsions. 

- behavioral_problems_in_school:
  * value: Set to true ONLY IF the text mentions behavioral issues, disciplinary actions, or acting out in school. This includes verbal reprimands, reported truancy, detention, complaints from teachers, or any other disciplinary measure that does not reach the threshold of suspension or expulsion. Do NOT set to true for academic difficulties or poor academic performance unless explicit evidence of behavioral problems. Set to false ONLY IF behavioral issues, disciplinary actions, or acting out in school are explicitly denied.
  * supporting_text: Verbatim text proving the history of behavioral problems. 

- academic_problems_in_school:
  * value: Set to true ONLY IF the text mentions academic difficulties or poor academic performance in school. This includes repeating a grade or school year, failing a course or grade, poor grades, academic probation, being held back, or other indicators of academic underachievement. Do NOT set to true for behavioral issues such as truancy, skipping class, inattentiveness, disruptive behavior, detention, teacher complaints, suspension, or expulsion unless there is explicit evidence of academic problems. Set to false ONLY IF academic difficulties are explicitly denied.
  * supporting_text: Verbatim text proving the history of academic problems.

- history_of_bullying:
  * value: Set to true ONLY IF the text indicates the evaluee bullied or intimidated others. This includes verbal, physical, relational, and emotional altercations toward peers, reports of bullying classmates, or being identified as the perpetrator of bullying. Do not include isolated fights or general aggression unless explicitly described as bullying. Set to false ONLY IF a history of bullying others is explicitly denied.
  * supporting_text: Verbatim text proving the history of bullying. 

- history_of_being_bullied:
  * value: Set to true ONLY IF the text indicates the evaluee was a victim of bullying. This includes being teased, harassed, intimidated, socially excluded, or subjected to repeated verbal, physical, or emotional aggression by peers. Do not include abuse or neglect perpetrated by caregivers. Set to false ONLY IF being bullied is explicitly denied.
  * supporting_text: Verbatim text proving the history of being bullied.

- current_employment_status:
  * value: The evaluee's employment status at the time of the evaluation. Output "Unemployment & Receiving Disability" when the evaluee is currently unemployed AND the text indicates that they are currently receiving disability benefits (Social Security Disability Insurance, Social Security Disability, or another clearly identified disability payment/benefit). Output "Full-Time" if the evaluee currently has a full-time job. Output "Part-Time" if the evaluee currently has a part-time job. Output "Seasonal" if the evaluee currently has seasonal employment or a job that occurs only during part of the year, such as summer or holiday employment. Output "Employed" if the evaluee currently has a job but not specified as any of the prior. Output "Full-time Student" if the evaluee is currently a full-time student and there is no higher-priority employment classification that applies. Output "Unemployed" ONLY when the evaluee is currently unemployed and there is NO evidence of current disability benefits that would qualify for "Unemployment & Receiving Disability". 
  * supporting_text: Verbatim text snippet confirming the employment status. This will likely appear near the terms “job”, “employee”, “employer”, or “career”. 

- longest_duration_of_employment:
  * value: The longest continuous period the evaluee held a single job, rounded to the nearest month. Compare all stated job durations (current and past) and select the longest one. Do NOT assume the current job is longest unless explicitly stated. Durations broken by less than or equal to one month of unemployment count as separate jobs.
  * supporting_text: Verbatim snippet confirming the duration of the longest job. Information related to this will often be found in a specific section entitled “Employment Hx”. 

- primary_industry_of_employment:
  * value: The main type of work, trade, or industry the evaluee has worked in for the longest period of time (e.g., "Construction", “Healthcare”, "Fast food", “Financial Services”, “Education”, “Military”, "Retail"). If evaluee has been employed in multiple industries, select the one that they have worked for the longest in, or is their primary career. 
  * supporting_text: Verbatim text snippet confirming the industry. This information will most likely be found in the “Employment Hx” section. Some documents include “Employer name” which can be used to determine the industry the patient works in. 

Important Extraction Rules:
- Verbatim Quotes Only: For any field requiring supporting_text, you MUST extract the exact, verbatim text snippet from the document that proves or contains the extracted value.
- No Verbatim Text: If there is no verbatim text supporting a value, do not infer or assign a value. Set the value and confidence to null.
- Missing Data (Null Rule): If a specific piece of information is completely missing from the text, you MUST output null for `value`, null for `supporting_text`, and null for `confidence`. 
- Confidence Scoring: Set confidence to "high" only if the verbatim text explicitly confirms the value. Set it to "medium" or "low" if there is ambiguity in the text or OCR errors. CRITICAL: NEVER output a confidence score (high/medium/low) if `supporting_text` is null. If there is no supporting text, the confidence MUST be null.
- Critical Boolean Rule: You must distinguish between "Denied" and "Not Mentioned". If a report explicitly says a history is denied, output false. If the report simply does not talk about it, you MUST output null for both the value and supporting_text.
- Current / Present indicators: Refers strictly to thoughts, behaviors, or symptoms occurring or observed *during the evaluation itself*. Look for explicit phrasing such as "currently," "at this time," "during the interview," "today," or present-tense clinical observations made by the evaluator.
- History / Past indicators: Refers strictly to anything that happened *prior to the evaluation*. Look for explicit phrasing such as "previously," "in the past," "history of," "used to," "prior episodes," or any events described as occurring before the current assessment.

- For the sections about family history and developmental history it can often be found under a specific section, either labeled “Marriage/Relationships/Children”, “Personal/Family Hx”, “Family History”, “Family, Personal, Educational, and Social History”, or particularly under the “Reared by” heading. It may also often be found near the terms “Learning d/o", “Developmental”, “Educational Hx”, “Personal”, “Family”, “Social”, “History”, and “Hx”.

Exclusion Criteria: 
- Number of Siblings: You MUST evaluate each family member individually. Count ONLY individuals explicitly identified as siblings (brother, sister, half‑brother, stepsister, etc.). Non‑siblings — including mother, father, aunt, uncle, cousin, grandparent — MUST NOT increase the sibling count. Plural non‑siblings (e.g., “three cousins,” “both parents”) MUST NOT trigger the ">=2" rule. When exactly one sibling is mentioned, the value MUST be "operator: =", "value: 1" even if other relatives are present. Apply the ">=2" rule ONLY when the plural noun explicitly refers to siblings.
- Current Household: EXCLUDE ALL living arrangements inside COUNTY JAIL. Any mention of living in jail, being housed in jail, or residing in jail MUST NOT be used to determine household status. Having children does NOT imply domicile. Null when housing is not actually stated, DON'T ASSUME. 
- Developmental Delay: You MUST NOT count general conditions such as autism spectrum disorder, intellectual disability, learning disorders, ADHD, ADD, ODD, or any purely behavioral/mood disorders as developmental delays, unless an explicit speech or motor delay is also detailed. 
- Current Household: Do NOT count the evaluee's current jail, prison, detention center, or current psychiatric hospitalization as their household status; you must capture the living situation strictly prior to the current arrest. Do NOT classify living with relatives as "Other".


Return JSON only. Do NOT wrap the JSON response in markdown code blocks (```json). Now analyze this OCR report excerpt:

{{report}}