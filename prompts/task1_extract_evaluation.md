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
- is_competence_to_stand_trial (boolean): Set to true if the document contains a competency evaluation report. Set to false and all remaining fields below to null if otherwise. 

- header (string): The exact text string of the title for the competence to stand trial report. Ignore # symbol in extraction.

- author (object):
  * value: Name of the physician/examiner (e.g., "Michael Fuller, MD").
  * supporting_text: Verbatim text snippet containing the author's name/signature line. If the author's name is in different line, return first line.

- cause_number (object):
  * value: The court cause/case number.
  * supporting_text: Verbatim text snippet showing the case/cause number designation. (e.g., Cause No. 12AB0345, Cause # 12AB0345)

- date_of_report (object):
  * value: The date the report was signed/written (formatted strictly as YYYY-MM-DD).
  * supporting_text: Verbatim phrase containing the report date (e.g., Date of Report: February 20, 2019).

- date_of_examination (object):
  * value: The date the actual clinical evaluation took place (formatted strictly as YYYY-MM-DD).
  * supporting_text: Verbatim phrase detailing the date of evaluation (e.g., Date of Evaluation: February 20, 2019).

- block_section_start (integer): The raw block number where the competency evaluation text begins. The beginning usually contains: the title/header, the author/examiner name ,cause number, court information, examination statement. 

- block_section_end (integer): Identify the LAST block section where the competency evaluation meaningfully ends. This should usually contain: competency opinions, treatment recommendations, other comments, examiner signatures, conclusions, and similiar. 

Important Extraction Rules:
- Verbatim Quotes Only: For any field requiring supporting_text, you MUST extract the exact, verbatim text snippet from the document that proves or contains the extracted value.
- Confidence Scoring: Set confidence to "high" only if the verbatim text explicitly and unambiguously confirms the value. Set it to "medium" or "low" if there is ambiguity, typos, or if you are inferring the value from messy OCR context.

Return JSON only. Do NOT wrap the JSON response in markdown code blocks (```json). Now analyze this OCR report:

{{report}}