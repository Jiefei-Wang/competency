#python -m pip install transformers openai llmrunner pandas pyarrow torch
#python -m pip install torch
#python -m pip install git+https://github.com/Jiefei-Wang/llmrunner.git
#python -m pip install git+https://github.com/Jiefei-Wang/extract_inspector.git
#python -m pip install llm_output_parser

from pathlib import Path
import asyncio
from openai import AsyncOpenAI
from tqdm import tqdm
from llm_output_parser import parse_json
from llmrunner import Runner, Task
from transformers import AutoTokenizer
import pandas as pd
import json
import os
import time

from modules.data_template_task1 import CompetencyReportExtraction
from modules.extractor_task1 import results_to_dataframe
from modules.vllm import get_model_name, llm_msg, clean_and_truncate_texts
from modules.validator_task1 import validate_competency_report_task



client = AsyncOpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1"
)

runner = Runner(
    client=client
)

MAX_TOKENS = 50000
# model_name = 'google/gemma-4-E2B-it'
model_name = asyncio.run(get_model_name(client))
tokenizer = AutoTokenizer.from_pretrained(model_name)

def runner_json(task):
    ok, reasons, parsed_data = validate_competency_report_task(task)
    if not ok and len(task.messages)<=6: # only retry twice (initial + 1 retry)
        validation_msg = "\n".join(reasons)
        print(f"task.index: {task.index}. Validation: {validation_msg}")
        task.messages.append({"role": "user", "content": validation_msg})
        return task

    return parsed_data


def extract_parsed_data(result):
    if isinstance(result, dict):
        return result
    output = getattr(result, "output", None)
    if isinstance(output, dict):
        return output
    if isinstance(output, str):
        try:
            parsed = parse_json(output, strict=False)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    return {}


with open("prompts/task1_extract_evaluation.md", "r") as f:
    prompt_template = f.read()

schema = CompetencyReportExtraction.model_json_schema()
prompt_template = prompt_template.replace("{schema}", json.dumps(schema, indent=2))

# need to duplicate on here 
with open("output/task1_extract_evaluation.md", "w") as f:
    f.write(prompt_template) 


note = pd.read_feather("output/pdf_md_ocr.feather")
all_note = note.text.tolist()
modified_notes = []

# Adding block sections
for i, text in enumerate(all_note):
    lines = text.splitlines()
    new_lines = []
    block_num = 1
    for j, line in enumerate(lines):
        if j % 50 == 0:
            new_lines.append(f"block section {block_num}")
            block_num += 1
        new_lines.append(line)
    final_text = "\n".join(new_lines)
    modified_notes.append(final_text)
    # with open(f"output/sample_notes/note_{i}.txt", "w", encoding="utf-8") as f:
    #     f.write(final_text)

texts = modified_notes[:100]
truncated_text = clean_and_truncate_texts(tokenizer, texts, MAX_TOKENS)

prompts = [prompt_template.replace("{{report}}", text) 
           for text in truncated_text
]

message_list = [llm_msg(prompt) for prompt in prompts]
tasks = [
    Task(messages=messages, 
         original = truncated_text[i],
         note_id = note.id[i]
         ) 
    for i, messages in enumerate(message_list)]


start_time = time.time()
results = runner.run(
    tasks,
    pipeline = [runner_json],
    model=model_name,
    temperature=0
)
end_time = time.time()

print(f"Extraction time: {end_time - start_time} seconds")
    
df = results_to_dataframe(results)
df.to_json("output/task1_extraction.jsonl", orient="records", lines=True)
df.to_feather("output/task1_extraction.feather")
df.to_csv("output/task1_extraction_review.csv", index=False)
print(df.head())



print("\nExtracting evaluation blocks to markdown files...")


output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

extracted_records = []

for i, task in enumerate(tasks):
    print(f"\n--- Document Note ID: {task.note_id} ---")
    parsed_data = extract_parsed_data(results[i])
    if not isinstance(parsed_data, dict) or not parsed_data:
        print("Skipped: Did not pass JSON validation.")
        continue     

    is_competency = parsed_data.get("is_competence_to_stand_trial")
    print(f"Is Competency Report?: {is_competency}")
    
    if is_competency:
        start_block = parsed_data.get("block_section_start")
        end_block = parsed_data.get("block_section_end")
        
        print(f"LLM extracted blocks: Start = {start_block}, End = {end_block}")
        if start_block and end_block:
            note_text = modified_notes[i]
            start_marker = f"block section {start_block}"
            next_marker = f"block section {end_block + 1}"
            start_idx = note_text.find(start_marker)
            end_idx = note_text.find(next_marker)
            
            if start_idx != -1:
                if end_idx != -1:
                    extracted_text = note_text[start_idx:end_idx].strip()
                    print(f"Sliced from {start_marker} to {next_marker}")
                else:
                    extracted_text = note_text[start_idx:].strip()
                    print(f"Sliced from {start_marker} to end of document")
                    
                extracted_records.append({
                    "note_id": task.note_id,
                    "block_section_start": start_block,
                    "block_section_end": end_block,
                    "evaluation_text": extracted_text
                })
            else:
                print(f"Error: Could not find exact text '{start_marker}' in the document.")
        else:
            print("Skipped: start_block or end_block was missing.")
    else:
        print("Skipped: Document is not a competency report.")
        


df_blocks = pd.DataFrame(extracted_records)
feather_path = "output/extraction_blocks.feather"
    
# Save to feather 
df_blocks.to_feather(feather_path)