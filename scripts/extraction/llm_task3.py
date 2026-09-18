#python -m pip install transformers openai llmrunner pandas pyarrow torch
#python -m pip install torch
#python -m pip install git+https://github.com/Jiefei-Wang/llmrunner.git
#python -m pip install git+https://github.com/Jiefei-Wang/extract_inspector.git
#python -m pip install llm_output_parser

#from scripts.extraction.llm_task3 import runner_json_task3

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

from modules.data_template_task3 import HistoryLegalCompetence
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
tokenizer = AutoTokenizer.from_pretrained("RedHatAI/gemma-4-26B-A4B-it-FP8-Dynamic")

with open("prompts/task3_extract_evaluation.md", "r", encoding="utf-8") as f: # encoding = "utf-8"?
    prompt_template = f.read()

schema = HistoryLegalCompetence.model_json_schema()
prompt_template = prompt_template.replace("{schema}", json.dumps(schema, indent=2))

# need to duplicate on here 
with open("output/task3_extract_evaluation.md", "w", encoding="utf-8") as f:
    f.write(prompt_template)
    
note = pd.read_feather("output/task1/extraction_blocks.feather")
all_note = note.evaluation_text.tolist()

texts = all_note[:50]
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

def runner_json_task3(task):
    return runner_json(task, HistoryLegalCompetence)

start_time = time.time()
results = runner.run(
    tasks,
    pipeline = [runner_json_task3],
    model=model_name, 
    temperature=0
)
end_time = time.time()

print(f"Extraction time: {end_time - start_time} seconds")

output_dir = "output/task3"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df = results_to_dataframe(results, HistoryLegalCompetence)
df = df.merge(note[['note_id', 'file_name']], on='note_id', how='left')
# move file_name column to the front
df = df[['file_name'] + [col for col in df.columns if col != 'file_name']]

df.to_json(f"{output_dir}/extraction.jsonl", orient="records", lines=True)
df.to_feather(f"{output_dir}/extraction.feather")
df.to_csv(f"{output_dir}/extraction_review.csv", index=False)
print(df.head())

# Review column: number_of_suicide_attempts
print(df['number_of_suicide_attempts_value'])

# Added task 1, 2, and 3
df1 = pd.read_feather("output/task1/extraction.feather")
df2 = pd.read_feather("output/task2/extraction.feather")
df3 = pd.read_feather("output/task3/extraction.feather")

df1 = df1.rename(columns={"note_id": "text_id"})
df2 = df2.rename(columns={"note_id": "text_id"})
df3 = df3.rename(columns={"note_id": "text_id"})

merged_df = df1.merge(df2, on="text_id", how="outer").merge(df3, on="text_id", how="outer")

merged_df.to_csv(f"output/extraction_1,2,3.csv", index=False)
merged_df.to_feather(f"output/extraction_1,2,3.feather")
