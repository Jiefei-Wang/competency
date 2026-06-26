#python -m pip install transformers openai llmrunner pandas pyarrow torch
#python -m pip install torch
#python -m pip install git+https://github.com/Jiefei-Wang/llmrunner.git
#python -m pip install git+https://github.com/Jiefei-Wang/extract_inspector.git
#python -m pip install llm_output_parser

import asyncio
from openai import AsyncOpenAI
from llmrunner import Runner, Task
from transformers import AutoTokenizer
import pandas as pd
import json
import os
import time

from modules.data_template_task1 import CompetencyReportExtraction
from modules.block import get_block_content, insert_block_num
from modules.extractor import results_to_dataframe
from modules.vllm import get_model_name, llm_msg, clean_and_truncate_texts, runner_json


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

with open("prompts/task1_extract_evaluation.md", "r") as f:
    prompt_template = f.read()

schema = CompetencyReportExtraction.model_json_schema()
prompt_template = prompt_template.replace("{schema}", json.dumps(schema, indent=2))

# need to duplicate on here 
with open("output/task1_extract_evaluation.md", "w") as f:
    f.write(prompt_template) 


note = pd.read_feather("output/pdf_md_ocr.feather")
all_note = note.text.tolist()
modified_notes = insert_block_num(all_note, n=50)

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


def runner_json_task1(task):
    return runner_json(task, CompetencyReportExtraction)

start_time = time.time()
results = runner.run(
    tasks,
    pipeline = [runner_json_task1],
    model=model_name,
    temperature=0
)
end_time = time.time()

print(f"Extraction time: {end_time - start_time} seconds")

output_dir = "output/task1"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df = results_to_dataframe(results, CompetencyReportExtraction)
df.to_feather(f"{output_dir}/extraction.feather")
df.to_json(f"{output_dir}/extraction.jsonl", orient="records", lines=True)
df.to_csv(f"{output_dir}/extraction_review.csv", index=False)
print(df.head())



print("\nExtracting evaluation blocks to markdown files...")

extracted_records = []
note_text_by_id = dict(zip(note.id.tolist(), modified_notes))

for _, row in df.iterrows():
    note_id = row["note_id"]
    print(f"\n--- Document Note ID: {note_id} ---")
    
    is_competency = row.get("is_competence_to_stand_trial")
    if is_competency:
        start_block = row.get("block_section_start")
        end_block = row.get("block_section_end")
        
        print(f"LLM extracted blocks: Start = {start_block}, End = {end_block}")
        note_text = note_text_by_id.get(note_id)
        if note_text is None:
            print("Skipped: could not find source note text.")
            continue

        extracted_text = get_block_content(note_text, start_block, end_block)
        if extracted_text is None:
            print("Skipped: start_block or end_block was missing.")
            continue

        extracted_records.append({
            "note_id": note_id,
            "block_section_start": start_block,
            "block_section_end": end_block,
            "evaluation_text": extracted_text
        })
        print(f"Sliced blocks {start_block} to {end_block}.")
        


df_blocks = pd.DataFrame(extracted_records)
df_blocks.to_feather(f"{output_dir}/extraction_blocks.feather")
