Extract the relationship, psychiatric, substance use, past medical, and legal history as well as the competence recommendation information from the Competence to Stand Trial evaluation reports.

Your output structure must strictly follow the schema template below:

{schema}

Below are the definitions for the data elements in the schema. For each object, you must provide the value, the verbatim supporting text, and a confidence score.

- current_marital_status:
  * value: The evaluee's current marital status. Output could be one of the following: "Single", "Married", "Divorced", "Separated", "Widowed".
  * supporting_text: Verbatim text confirming the marital status.

- total_marriages:
  * value: The total number of times the evaluee has been married, including past and current marriages. Multiple marriages to the same partner count separately.
  * supporting_text: Verbatim text proving the total number of marriages.

- total_divorces:
  * value: The total number of times the evaluee has been divorced or legal separation. Multiple divorces from the same partner count separately. If evaluee never married then output null.
  * supporting_text: Verbatim text proving the total number of divorces.

- number_of_children:
  * value: The total number of children, living or dead, the evaluee has. Includes biological, adopted, and step-children if the evaluee had legal guardianship or lived with them.
  * supporting_text: Verbatim text confirming the number of children.

- current_psychiatric_diagnosis:
  * value: The evaluee's primary or most relevant current psychiatric condition (excluding substance use disorders). Output one of the following: "Neurodevelopmental Disorders", "Schizophrenia Spectrum and Other Psychotic Disorders", "Bipolar and Related Disorders", "Depressive Disorders", "Anxiety Disorders", "Obsessive-Compulsive and Related Disorders", "Trauma- and Stressor-Related Disorders", "Dissociative Disorders", "Somatic Symptoms and Related Disorders", "Feeding and Eating Disorders", "Elimination Disorders", "Sleep-Wake Disorders", "Sexual Dysfunction", "Gender Dysphoria", "Disruptive, Impulse-Control, and Conduct Disorders", "Neurocognitive Disorders", "Personality Disorders", "Paraphilic Disorders", "Other Mental Disorders", "Adverse Effects of Medication", or "Other".
  * supporting_text: Verbatim text confirming the diagnosis.

- current_psychiatric_medications:
  * value: All psychiatric medications the evaluee is currently prescribed and/or taking. Include any medications relevant to psychiatry or the treatment of mental health conditions (antidepressants, antipsychotics, mood stabilizers, sleep medications, or prescription stimulants). Include generic and brand names if given. If there are no medications currently prescribed in the record, AND the evaluee states they have never used a psychiatric medication, the output should be "Never Used".
  * supporting_text: Verbatim text listing the medications.

- number_of_psychiatric_hospitalizations:
  * value: The total number of times the evaluee has been admitted to inpatient psychiatric care such as “Psych Ward” or other inpatient facility (voluntary or involuntary).
  * supporting_text: Verbatim text proving the number of hospitalizations.

- history_of_suicide_thoughts:
  * value: Set to true ONLY if the text documents a past, historical episode of expressing suicidal thoughts, ideation, plans, intent, death wishes, or thoughts that they would be better off dead occurring prior to the current evaluation. Do NOT set to true based solely on current/present thoughts or recent placement measures unless past history is explicitly stated. Set to false if the text explicitly denies a past history (e.g., "denied any PAST suicide attempts/thoughts").
  * supporting_text: Verbatim text confirming the past/historical suicidal thoughts.

- history_of_self_harm_behavior:
  * value: Set to true ONLY if the evaluee has a documented past history of intentionally engaging in self-harming behavior prior to the evaluation, EXCLUDING suicide attempts and accidental injuries. Do NOT include self-harming behavior described as currently occurring. Set to false if the evaluee explicitly denies a past history of self-harm.
  * supporting_text: Verbatim text confirming the past/historical self-harm behavior.

- number_of_suicide_attempts:
  * value: The total number of lifetime suicide attempts, regardless of physical harm or hospitalization (DO NOT INCLUDE accidental overdose). If an exact count is provided, output the integer. If the text states "multiple suicide attempts," "several attempts," or similar phrasing without a precise number, output the operator ">=" and the integer 2. If the evaluee explicitly denies attempts, output "0".
  * supporting_text: Verbatim text proving the number or qualitative description of attempts.

- history_of_violence:
  * value: Set to true ONLY if the evaluee has a history of violence towards others (inflicting physical or sexual damage to unwilling victim, people or animals, or fighting unless consistently the victim). DOES NOT include the evaluee's current legal charge(s). Set to false ONLY if history of violence is denied.
  * supporting_text: Verbatim text confirming violence history.

- substance_use_disorder_diagnosis:
  * value: This will include all diagnosed substance use disorders (DSM-V or equivalent) that the evaluee has. Exclude casual use without a diagnosed disorder. Output from the following: "Alcohol-Related Disorders", "Caffeine-Related Disorders", "Cannabis-Related Disorders", "Hallucinogen-Related Disorders", "Inhalant-Related Disorders", "Opioid-Related Disorders", "Sedative-, Hypnotic-, or Anxiolytic-Related Disorders", "Stimulant-Related Disorders", "Tobacco-Related Disorders", or "Other (or Unknown) Substance–Related Disorders".
  * supporting_text: Verbatim text confirming the diagnosed substance use disorder(s).

- type_of_substance_used:
  * value: All substance categories the evaluee currently uses or has used in the past. Includes both diagnosed disorders and recreational/casual use. Group the substances the evaluee has used/is using into: "Alcohol", "Caffeine", "Cannabis", "Hallucinogens", "Inhalants", "Opioids", "Sedatives/Hypnotics/Anxiolytics", "Stimulants", "Tobacco", or "Other (or Unknown)".
  * supporting_text: Verbatim text listing the history of substances used.

- age_of_first_use:
  * value: The earliest age at which the evaluee first used any recreational substance or drug. If multiple substances were used, output the age of the very first instance. EXCLUDE caffeine or authorized medical use.
  * supporting_text: Verbatim text confirming the age of first substance use.

- most_recent_use:
  * value:The number of months PRIOR to the date of the evaluation that the evaluee last used any substance/drug. EXCLUDE caffeine and authorized medical use. Output represents the total months.
  * supporting_text: Verbatim text proving the most recent timeline or date of use.

- prior_psychiatric_diagnosis:
  * value: All PSYCHIATRIC diagnoses given to the evaluee prior to the time of evaluation (excluding substance use disorders). Sort all of the evaluee's past psychiatric diagnoses into: "Neurodevelopmental Disorders", "Schizophrenia Spectrum and Other Psychotic Disorders", "Bipolar and Related Disorders", "Depressive Disorders", "Anxiety Disorders", "Obsessive-Compulsive and Related Disorders", "Trauma- and Stressor-Related Disorders", "Dissociative Disorders", "Somatic Symptoms and Related Disorders", "Feeding and Eating Disorders", "Elimination Disorders", "Sleep-Wake Disorders", "Sexual Dysfunction", "Gender Dysphoria", "Disruptive, Impulse-Control, and Conduct Disorders", "Neurocognitive Disorders", "Personality Disorders", "Paraphilic Disorders", "Other Mental Disorders", or "Adverse Effects of Medication".
  * supporting_text: Verbatim text confirming the past psychiatric diagnoses.

- prior_diagnosis:
  * value: All past MEDICAL conditions based on the primarily implicated cause/organ system. Output from the following: "Infectious Disease", "Neoplasms", "Immune Mechanism", "Endocrine/Nutritional/Diabetes", "Mental/Behavior", "Nervous System", "Eye", "Ear/Mastoid Process", "Circulatory System", "Respiratory System", "Digestive System", "Skin/Subcutaneous Tissue", "Musculoskeletal System/Connective Tissue", "Genitourinary System", "Pregnancy/Childbirth/Puerperium", "Perinatal", "Congenital/Chromosomal Abnormalities", "Injury/Poisoning/External Causes", or "Factors Influencing Health Status".
  * supporting_text: Verbatim text confirming the past medical diagnoses.

- current_medications:
  * value: All medications (medical and psychiatric) the evaluee is currently prescribed and/or taking. Include generic and brand names if given. If the patient explicitly states they has never used any medications, the output should be “None”.
  * supporting_text: Verbatim text listing the current medications.

- number_of_arrests:
  * value: The total number of times the evaluee has been arrested or detained by law enforcement, regardless of whether it led to charges or convictions. If evaluee states never arrested, output 0. If unknown, output 1 (assuming at least one recent arrest for this competency evaluation).
  * supporting_text: Verbatim text proving the number of arrests.

- number_of_incarcerations:
  * value: The number of distinct times the evaluee has been confined to a jail, prison, or equivalent detainment facility for at least 72 hours (excluding non-court-ordered mental health facilities).
  * supporting_text: Verbatim text proving the number of incarcerations.

- total_time_incarcerated:
  * value: The total lifetime duration the evaluee has spent incarcerated, in months. This includes both historical incarcerations and the current ongoing period of incarceration leading up to the evaluation. You MUST account for the current arrest. If the evaluation provides an arrest date or timeframe (e.g., arrested on a specific date or "arrested in [Month/Year]") and indicates ongoing detention using phrases like "has been detained since," "in custody since," "remains in jail," or "incarcerated since," calculate the time between that arrest date and the examination date in months (e.g., Feb 23 to May 29 = ~3 months). ADD this ongoing duration to any past incarceration time. Include all jail/prison stays of 72 hours or more. Exclude non-court-ordered mental health facilities.
  * supporting_text: Verbatim text confirming the total time incarcerated.

- history_of_prior_charges:
  * value: Set to true ONLY if the evaluee has ever been arrested, accused, or formally charged with a crime in the past, REGARDLESS of the final outcome (includes dismissed, dropped, or acquitted charges). Set to false ONLY if a history of prior charges or arrests is explicitly denied.
  * supporting_text: Verbatim text confirming the presence or absence of prior charges.

- number_of_prior_charges:
  * value: The total number of times the evaluee has been formally accused, charged, or arrested for a crime, REGARDLESS of the final outcome. This includes all past charges, whether they were dropped, dismissed, resulted in an acquittal, or led to a conviction. If the evaluee states they have never been charged/arrested, output 0.
  * supporting_text: Verbatim text proving the total number of prior charges or arrests.

- history_of_prior_convictions:
  * value: Set to true ONLY if the evaluee has ever been formally found GUILTY, pled guilty, or pled no contest to a crime in the past. Do NOT trigger true for mere arrests, dismissed charges, or current pending charges. Set to false ONLY if prior convictions are explicitly denied.
  * supporting_text: Verbatim text confirming the presence or absence of prior convictions.

- number_of_prior_convictions:
  * value: The total number of prior crimes where the evaluee was formally found GUILTY, pled guilty, or pled no contest. Do NOT include current pending charges or past charges that were dismissed/dropped. Multiple convictions in a single trial count separately. If evaluee states never convicted, output 0.
  * supporting_text: Verbatim text proving the total number of prior convictions.

- number_of_competency_exams:
  * value: The total number of competency to stand trial exams the evaluee has undergone PRIOR to the current evaluation. If evaluee mentions that they have never undergone one before, output 0.
  * supporting_text: Verbatim text proving the number of prior competency exams.

- number_of_times_found_incompetent:
  * value: The total number of times the evaluee has been found incompetent or not competent in a competency to stand trial exam PRIOR to the current evaluation. If never found incompetent, output 0.
  * supporting_text: Verbatim text proving the number of times found incompetent.

- age_at_first_crime:
  * value: The evaluee's age at which they committed their first crime. Only consider crimes that led to a conviction/settlement or that the evaluee fully admits to (do NOT count current unproven charges unless admitted). If evaluee states no past crimes, output 0.
  * supporting_text: Verbatim text proving the age at the first crime.

- depressive_symptoms:
  * value: Set to true ONLY if the evaluee is currently expressing any depressive symptoms. (e.g., depressed mood, incapacitating feelings of sadness/emptiness/loneliness, diminished pleasure/anhedonia, significant weight loss/gain, insomnia, hypersomnia, psychomotor agitation, psychomotor retardation, fatigue/daily low energy, feelings of worthlessness/guilt, decreased capacity to concentrate, recurrent thoughts of death, or suicidal ideation). Set to false ONLY if depressive symptoms are denied.
  * supporting_text: Verbatim text confirming the presence or absence of depressive symptoms.

- manic_symptoms:
  * value: Set to true ONLY if the evaluee is currently expressing any manic symptoms (e.g., elevated/expansive/irritable mood, inflated self-esteem/grandiosity, decreased need for sleep, more talkative than baseline, flight of ideas, racing thoughts, distractibility, or increase in goal-directed/risky activities). Set to false ONLY if any manic symptoms are explicitly denied.
  * supporting_text: Verbatim text confirming the presence or absence of manic symptoms.

- anxiety_symptoms:
  * value: Set to true ONLY if the evaluee is currently expressing any anxious symptoms (e.g., social anxiety, unexpected panic attacks, agoraphobia, excessive anxiety/worry, restlessness, on edge, easily fatigued, poor concentration, irritability, muscle tension, or difficulty falling/staying asleep). Set to false ONLY if anxiety symptomsare denied.
  * supporting_text: Verbatim text confirming the presence or absence of anxiety symptoms.

- PTSD_symptoms:
  * value: Set to true ONLY if the evaluee is currently expressing any symptoms characteristic of PTSD (e.g., intrusive memories, nightmares, flashbacks, distress or avoidance regarding reminders of trauma, negative beliefs about oneself, persistent negative emotional state, anhedonia, detachment, persistent inability to feel positive emotions, hypervigilance, exaggerated startle response, or poor concentration/sleep). Set to false if PTSD symptoms are denied.
  * supporting_text: Verbatim text confirming the presence or absence of PTSD symptoms.

- psychotic_symptoms:
  * value: Set to true ONLY if the evaluee is currently expressing any psychotic symptoms (e.g., visual/auditory/olfactory/somatic hallucinations, disorganized speech/thoughts/behavior, bizarre appearance, catatonia, "negative symptoms", flat affect, diminished emotional expression, poor eye contact, poverty of speech/thought, thought blocking, or delusions). Set to false ONLY if psychotic symptoms are denied.
  * supporting_text: Verbatim text confirming the presence or absence of psychotic symptoms.

- suicidal_ideation_behavior:
  * value: Set to true ONLY when the text indicates that the evaluee is experiencing active suicidal thoughts, suicidal ideation, suicidal intent, or a suicide plan at the time of the evaluation. Set to false if the text only mentions past/historical thoughts, or if current suicidal ideation is explicitly denied (e.g., "denied current suicidal or homicidal ideation").
  * supporting_text: Verbatim text explicitly describing the evaluee's current suicidal thoughts, ideation, intent, or plan.

- agitated_behavior:
  * value: Set to true ONLY if the evaluee is currently expressing agitated behavior (e.g., inability to sit still, pacing, handwringing, trembling, loud/pressured speech, or angry/upset affect). Set to false ONLY if agitated behavior is denied.
  * supporting_text: Verbatim text confirming the presence or absence of agitated behavior.

- violence_agression:
  * value: Set to true ONLY if the evaluee is currently expressing any violent or aggressive symptoms/behaviors (e.g., yelling, threatening, attempting physical violence, throwing objects, pacing, inability to calm down, or angry/rageful affect). Set to false ONLY if violence agression is denied.
  * supporting_text: Verbatim text confirming the presence or absence of violent or aggressive behavior.

- factual_understanding:
  * value: Set to true if the evaluee possesses sufficient factual understanding to participate in a trial, OR if graded as "Above Average", "Average", or "Below Average". Set to false if factual understanding is explicitly denied, deemed insufficient, OR if graded as "Poor" or "Very Poor".
  * supporting_text: Verbatim text confirming the factual understanding.

- rational_understanding:
  * value: Set to true if the evaluee possesses a sufficient rational understanding of the legal process to participate in a trial, OR if graded as "Above Average", "Average", or "Below Average". Set to false if rational understanding is explicitly denied, deemed insufficient, OR if graded as "Poor" or "Very Poor".
  * supporting_text: Verbatim text confirming the rational understanding.

- ability_to_assist_in_own_defense:
  * value: Set to true if the evaluee possesses the capacity to assist in their own defense in a trial, OR if graded as "Above Average", "Average", or "Below Average". Set to false if it is stated that the evaluee cannot assist in their own defense, OR if graded as "Poor" or "Very Poor".  
  * supporting_text: Verbatim text confirming the capacity to assist in defense.

- competent_to_stand_trial:
  * value: Set to true ONLY if the final outcome concludes the evaluee has the capacity/is competent to stand trial. Set to false ONLY if the exam concludes they are NOT competent/incompetent.
  * supporting_text: Verbatim text confirming the final competency finding.

- restorable_if_incompetent:
  * value: Set to true ONLY if a patient deemed incompetent is potentially restorable (could meet criteria in the future given intervention). Set to false ONLY if stated that they are unlikely/unable to ever meet capacity again.
  * supporting_text: Verbatim text confirming restorability potential.


Important Extraction Rules
- Current / Present: Refers strictly to thoughts, behaviors, or symptoms occurring or observed *during the evaluation itself*. Look for explicit phrasing such as "currently," "at this time," "during the interview," "today," or present-tense clinical observations made by the evaluator.
- History / Past: Refers strictly to anything that happened *prior to the evaluation*. Look for explicit phrasing such as "previously," "in the past," "history of," "used to," "prior episodes," or any events described as occurring before the current assessment.
- Mutual Exclusivity (No Assumptions): You must treat past and present timelines as strictly separate. A current symptom does NOT automatically justify a "history" field. A past symptom does NOT automatically justify a "current" field. Each field must be independently justified by explicit text. Do not infer past states from present states, or vice versa.
- Missing Data (Null Rule): If a specific piece of information is completely missing from the text, you MUST output null for `value`, null for `supporting_text`, and null for `confidence`. 
- Confidence Scoring: Set confidence to "high" only if the verbatim text explicitly confirms the value. Set it to "medium" or "low" if there is ambiguity in the text or OCR errors. CRITICAL: NEVER output a confidence score (high/medium/low) if `supporting_text` is null. If there is no supporting text, the confidence MUST be null.
- No Verbatim Text: If there is no verbatim text supporting a value, do not infer or assign a value. Set the value and confidence to null.
- Restorability if competent: If `competent_to_stand_trial` is true, this value MUST be null.


Formatting for multiple value extraction
- Always extract prescribed medications, diagnoses, or active treatment plans regardless of the evaluee's compliance. If a provider formally prescribed or diagnosed it, include it in your output even if the text explicitly notes the evaluee is noncompliant, refusing treatment, or not currently taking the medication
- If there are NO medications currently prescribed or noted in the medical record, AND the evaluee states they have never used a psychiatric medication, the output should be "Never Used".
- Use a comma followed by a space (`, `) to separate distinct, individual items in a list (e.g., "Depressive Disorders, Anxiety Disorders" or "Cannabis, Tobacco").
- Use a forward slash (`/`) with no spaces to separate generic and brand names of the same medication, or alternate terms for a single concept (e.g., "fluoxetine/Prozac, alprazolam/Xanax").


Information Location
- Relationships and children: Look in the "Marriage/Relationships/Children" section, or near terms like "dependent", "dependents", "Personal", "Social", "History", and "Hx".
- Psychiatric diagnoses, medications and hospitalizations: Typically found near "diagnosis", "Clinical Impression", "Mental Health Treatment Hx", "Inpt?", "Medical Hx" or specific "Medication" forms.
- Past/current medical diagnoses: Found under "Learning d/o", "Medical Hx", "Mental Health Treatment Hx", "Inpt?", "Outpt?", "Past Psychiatric History", "PMH", "Past Medical History". May be in medication lists, as diagnoses are often listed as reasons for the prescription.
- Substance use: Evaluee's past medical history or social history, as well as near the terms “Substance Abuse Hx”, “Medical Hx”, “Mental Health Treatment Hx”, “Drug test results”, “Drug Test History”, or “Alcohol/Drug Use:".
- Suicidal thoughts, ideation and attempts: Found under "Preoccupation", "Suicide and Other Risk Factors", "Suicide Risk", "Suicide Risk Level", and "Suicide Ideation". Look in the mental status exam, specifically under "Behavior/Attitude", "Emotional State", "Disturbance of Thought", "Preoccupation", or "Death Wishes".
- Self-harm: Mentions may be evaluee admissions or evaluator observations. Look under "Disturbance of Thought and Preoccupation", "History of Self Harm", "Social Hx", or sections discussing stress and coping.
- History of violence: Search broadly across "Educational Hx", "Learning d/o", "Employment Hx", "Substance Abuse Hx", "Marriage/Relationships/Children", "Mental Health Treatment Hx", "Inpt?", "Oupt?", "Arrests", "Convictions", "Current parole or probation", "Behavior/Attitude", "Preoccupation", or near the phrase "homicidal ideation".
- Legal history (charges, arrests, convictions): Typically found near the words "Offence", "Crime Incident(s)", "Current Charges", "Charge", or "Charges". Also located under sections titled "LEGAL HX", "Legal History", "Arrests", "Convictions", or "TDCJ".
- Prior competency exams: Look under "LEGAL HX", "Legal History", "Convictions", "Mental Health Treatment Hx", "Inpt", "Social Hx", or within mentions of the patient's judicial record.
- Depressive and psychotic symptoms: Look in the mental status exam. Specific subsections include "Appearance", "Attire", "Hygiene", "Grooming", "Eye Contact", "Behavior/Attitude", "Emotional State", "Affect" (especially if noted as "flat"), "Mood", "Motor Activity", "Thought Process", "Disturbance of Thought", "Delusional Ideations", "Perceptual Disturbances", and "Hallucinations".
- Other symptoms (manic, anxiety, PTSD, agitated, aggressive): Look in the mental status exam, often under "Behavior/Attitude", "Emotional State", "Affect", "Mood", "Disturbance of Thought", "Preoccupation", "Speech" (Rate/Volume), "Motor Activity", and "Thought Content" (especially near "grandiose").
- Competence Recommendations: Look in the final evaluation near "Summary of findings", "Issues/Factors considered...", or "Opinion of competency...". Look for specific phrases regarding capacity to understand the adversarial nature, capacity to consult with counsel, or treatment recommendations (for restorability).


Return JSON only. Do NOT wrap the JSON response in markdown code blocks (```json). Now analyze this OCR report excerpt:

{{report}} 

