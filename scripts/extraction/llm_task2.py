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

from modules.data_template_task2 import SocioeconomicFamilyExtraction
from modules.extractor_task2 import results_to_dataframe
from modules.vllm import get_model_name, llm_msg, clean_and_truncate_texts
from modules.validator_task2 import validate_socioeconomic_family_task

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
    ok, reasons, parsed_data = validate_socioeconomic_family_task(task)
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

with open("prompts/task2_extract_evaluation.md", "r", encoding="utf-8") as f: # encoding = "utf-8"?
    prompt_template = f.read()

schema = SocioeconomicFamilyExtraction.model_json_schema()
prompt_template = prompt_template.replace("{schema}", json.dumps(schema, indent=2))

# need to duplicate on here 
with open("output/task2_extract_evaluation.md", "w") as f:
    f.write(prompt_template) 

note = pd.read_feather("output/extraction_blocks.feather")
all_note = note.evaluation_text.tolist()

texts = all_note[:100]
truncated_text = clean_and_truncate_texts(tokenizer, texts, MAX_TOKENS)

prompts = [prompt_template.replace("{{report}}", text) 
           for text in truncated_text]

message_list = [llm_msg(prompt) for prompt in prompts]

tasks = [
    Task(messages=messages, 
         original = truncated_text[i],
         note_id = note.iloc[i]['note_id']
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
df.to_json("output/task2_extractions.jsonl", orient="records", lines=True)
df.to_feather("output/task2_extractions.feather")
df.to_csv("output/task2_extractions_review.csv", index=False)
print(df.head())


df = pd.read_feather("output/task2_extractions.feather")
# Run Dashboard
from dashboard_repo.cst_reviewer import launch_dashboard

# Launch the UI programmatically 
launch_dashboard(notes_df=note, extracts_df=df)