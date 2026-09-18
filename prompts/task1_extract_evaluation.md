Extract the information about a competence to stand trial evaluation report.

A Competence to Stand Trial report is a formal psychiatric or forensic evaluation that addresses whether the defendant is mentally capable of participating in legal proceedings. It is NOT an order, a referral, or a sanity evaluation.

Competence to stand trial IS:

- Report of Psychiatric Examination
- Competency Evaluation Report
- Fitness to Proceed
- Competence to Stand Trial Report

Competence to stand trial report is NOT:

- an order. An order is merely a court request for an evaluation.
- an interview worksheet such as "Interview Worksheet for Competency to Stand Trial"
- an informed consent such as "INFORMED CONSENT FOR COURT DIRECTED PSYCHIATRIC EVALUATIONS", "Consent for Evaluation"
- a referral such as "..."
- a sanity evaluation. A sanity evaluation addresses whether the defendant was mentally responsible at the time of the crime.

Your output structure must follow the schema template below:
{schema}

Below are the definitions for the data elements in the schema:

- is_competence_to_stand_trial: Set to true if the document contains a competency evaluation report. Set to false and all remaining fields below to null if otherwise.
- header: The exact text string of the title for the competence to stand trial report. Ignore # symbol in extraction.

- examiner:
  * value: Name of the physician/examiner (e.g., "Michael Fuller, MD").
  * supporting_text: Verbatim text snippet containing the author's name/signature line. If the author's name is in different line, return first line.

- cause_number:
  * value: The court cause/case number.
  * supporting_text: Verbatim text snippet showing the case/cause number designation. (e.g., Cause No. 12AB0345, Cause # 12AB0345)

- date_of_report:
  * value: The date the report was signed/written (formatted strictly as YYYY-MM-DD).
  * supporting_text: Verbatim phrase containing the report date (e.g., Date of Report: February 20, 2019).

- date_of_examination:
  * value: The date the actual clinical evaluation took place (formatted strictly as YYYY-MM-DD).
  * supporting_text: Verbatim phrase detailing the date of evaluation (e.g., Date of Evaluation: February 20, 2019).

- court_county:
  * value: The name of the county in which the specific court facilitating the case is located. Output ONLY the name of the county (e.g., output "Galveston" rather than "Galveston County").
  * supporting_text: Verbatim text confirming the court county.

- court_number:
  * value: The number of the specific court managing the patient's case. Output as a whole number integer.
  * supporting_text: Verbatim text confirming the court number.

- evaluation_location:
  * value: The specific name, building, institution, or geographic location where the evaluation took place. The name of the facility is preferred if that is all that is provided ("Galveston County Jail, Texas", "Brazoria County Detention Center", or a local clinic).
  * supporting_text: Verbatim text confirming the evaluation address or location name.

- facility_type:
  * value: The general classification or type of facility where the evaluation occurred ("Jail", "Prison", "Detention Center", "Hospital", or "Outpatient Clinic").
  * supporting_text: Verbatim text confirming the facility type.

- currently_incarcerated:
  * value: Set to true if the evaluee is currently incarcerated (jail, prison, or secure detention facility) at the time of the evaluation. Set to false ONLY if they are explicitly stated to be out of custody (released on bond, living at home, clinic, or outpatient).
  * supporting_text: Verbatim text confirming the current incarceration status.

- examiner_qualifications:
  * value: The qualifications of the examiner conducting the assessment (e.g., MD, PHD, PsyD). If multiple, separate them with a forward slash and no spaces (e.g., MD/PHD). If no qualification is stated but the examiner is referred to as "Dr.", output "MD or DO". Do NOT use any periods or commas in the output.
  * supporting_text: Verbatim text confirming the examiner's qualifications.

- block_section_start: The raw block number where the competency evaluation text begins. The beginning usually contains: the title/header, the author/examiner name ,cause number, court information, examination statement.

- block_section_end: Identify the LAST block section where the competency evaluation meaningfully ends. This should usually contain: competency opinions, treatment recommendations, other comments, examiner signatures, conclusions, and similiar.

Important Extraction Rules:
- Verbatim Quotes Only: For any field requiring supporting_text, you MUST extract the exact, verbatim text snippet from the document that proves or contains the extracted value.
- Confidence Scoring: Set confidence to "high" only if the verbatim text explicitly and unambiguously confirms the value. Set it to "medium" or "low" if there is ambiguity, typos, or if you are inferring the value from messy OCR context.
- Missing Data (Null Rule): If a specific piece of information is completely missing from the text, you MUST output null for `value`, null for `supporting_text`, and null for `confidence`.
- Confidence Scoring: Set confidence to "high" only if the verbatim text explicitly confirms the value. Set it to "medium" or "low" if there is ambiguity in the text or OCR errors. CRITICAL: NEVER output a confidence score (high/medium/low) if `supporting_text` is null. If there is no supporting text, the confidence MUST be null.

Return JSON only. Do NOT wrap the JSON response in markdown code blocks (```json). Now analyze this OCR report:

{{report}}
