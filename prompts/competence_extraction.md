You are reviewing a single OCR-derived forensic or medical report. OCR text may be noisy, contain spelling errors, broken formatting, duplicated text, missing punctuation, incorrect line breaks, and misrecognized words. Be robust to these issues. Do not require exact wording when the meaning is clear.

## Task 1: Identify the Report Type

Decide whether the document CONTAINS a competence-to-stand-trial evaluation result anywhere in the text.

A Competence to Stand Trial report is a formal psychiatric or forensic evaluation that addresses whether the defendant is mentally capable of participating in legal proceedings. It is NOT an order, a referral, or a sanity evaluation.

Strong indicators that the document IS a Competence to Stand Trial report:
- A header or title such as "Competence to Stand Trial Report", "Competency to Stand Trial Report", "Competency Report", or similar
- Author is a physician (MD or DO); most reports are written by Michael Fuller or Stephen Baughn
- A stated reason for evaluation that is examination or evaluation of competence to stand trial
- Presence of an explicit "Opinion" or "Conclusion" section addressing competence to stand trial
- Presence of structured background history sections (birth, family, education, employment, legal, psychiatric, substance use, medical)
- A Mental Status Examination section
- A section on current or present charges
- A section explicitly labeled "Areas of Competency" or similar
- A Recommendations section
- Identification information: evaluee's name, date of birth, cause/case/criminal number
- Dates: date of examination and date of report

Not all elements need to be present. Use the overall pattern to judge intent and document type.

Important exclusion rules:
1. Do NOT classify a competence order as a competence result. An order is merely a court request for an evaluation, not the evaluation itself.
2. Do NOT classify a Sanity Evaluation as a competence result. A sanity evaluation addresses whether the defendant was mentally responsible at the time of the crime — not whether the defendant can stand trial.

---

## Task 2: Extract Report Content (only if the document IS a Competence to Stand Trial report)

If `contain_competence_result` is "yes", extract the fields below. Be tolerant of OCR noise and formatting irregularities.

If `contain_competence_result` is "no", return `"contain_competence_result": "no"` and set every other field in the schema to null.

## Output object rules

Most extracted fields use this object shape:

```json
{
  "value": "extracted value, summarized value, or list of strings",
  "supporting_text": "brief exact text span from the OCR that supports the value",
  "confidence": "high"
}
```

Date fields use this object shape:

```json
{
  "date_text": "date as written in the OCR text",
  "date_precision": "day",
  "date_day": 15,
  "date_month": 7,
  "date_year": 2012,
  "supporting_text": "brief exact text span from the OCR that supports the date",
  "confidence": "high"
}
```

Rules for all extracted field objects:
- Use the exact schema keys only. Do not add extra keys.
- Set the entire field to null when the information is absent, irrelevant, or cannot be determined.
- `supporting_text` should be a short quotation or near-exact OCR span from the report, not a paraphrase. Use null only when the value is clearly inferable but no compact supporting span can be isolated.
- `confidence` must be one of "high", "medium", or "low".
- Use "high" when the value is directly stated and OCR is clear.
- Use "medium" when the value is directly stated but OCR is noisy, fragmented, or requires minor normalization.
- Use "low" when the value is inferred from context or the OCR is ambiguous.
- For non-date fields, `value` must be either a string, an array of strings, or null, matching the field definition below.
- Do not invent facts. Do not fill a field from general knowledge or from another document.

Rules for date fields:
- Date fields are `date_of_examination`, `date_of_report`, and `evaluee_dob`.
- `date_text` is the date as written or best normalized from the OCR text.
- `date_precision` must be "day", "month", or "year".
- If a full date is available, set `date_precision` to "day" and populate `date_day`, `date_month`, and `date_year`.
- If only month and year are available, set `date_precision` to "month", set `date_day` to null, and populate `date_month` and `date_year`.
- If only year is available, set `date_precision` to "year", set `date_day` and `date_month` to null, and populate `date_year`.
- If the date is absent or cannot be interpreted, set the entire date field to null.
- Use integers for `date_day`, `date_month`, and `date_year`; do not use strings.

Field definitions:

- `header`: Title of the report exactly as it appears in the document; preserve original wording in one line.
- `author`: Full name and credentials of the report author; normalize when clear, e.g. "Michael Fuller, M.D.".
- `date_of_examination`: Date when the interview, examination, or evaluation took place.
- `date_of_report`: Date when the report was submitted, completed, dictated, or signed.
- `cause_number`: Cause, case, or criminal number exactly as it appears in the document.
- `evaluee_name`: Full name of the evaluated person; normalize to "LAST, FIRST MIDDLE" when possible.
- `evaluee_dob`: Date of birth of the evaluated person.
- `reason_for_evaluation`: One concise sentence stating why the evaluation was requested.
- `current_charges`: Array of concise criminal charge labels, e.g. ["Murder", "Aggravated Assault"].
- `birth_place`: City and state/country where the evaluee was born when available.
- `family`: Brief structured summary of family composition and upbringing.
- `childhood_development`: Brief summary of notable developmental history; use null if absent or explicitly unremarkable with no details.
- `education`: Highest level of education completed and school or district if known.
- `employment`: Array of employment history entries, each as a concise string with job, employer, and dates or period when available.
- `legal_history`: Array of prior legal involvement entries, each as a concise string with offense, jurisdiction, and year or period when available.
- `military_history`: Military service summary; use null if absent or if the report states no military service.
- `psychiatric_history`: Array of prior psychiatric diagnoses, hospitalizations, treatments, or significant symptoms.
- `substance_use`: Array of substances and usage patterns or history.
- `medical_history`: Array of significant medical conditions, procedures, injuries, or medications when clinically relevant.
- `mental_status_examination`: Concise structured summary of notable mental status findings, including appearance, behavior, speech, mood, affect, thought process, thought content, cognition, insight, and judgment when available.
- `areas_of_competency`: Concise summary of competency domains assessed and findings, such as understanding charges, court roles, proceedings, plea options, and ability to assist counsel.
- `opinion`: One to two sentences stating the clinician's competency determination and the main reason if provided.
- `recommendations`: Concise summary of recommendations, such as restoration treatment, inpatient care, outpatient care, medication, or further evaluation.

---

## Return Format

Use this output schema exactly:

{schema}

Rules:
- Return JSON only.

Now analyze this OCR report:

{{report}}
