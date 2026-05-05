# pip install git+https://github.com/Jiefei-Wang/llmrunner.git
# pip install git+https://github.com/Jiefei-Wang/extract_inspector.git
from pathlib import Path
import asyncio
from openai import AsyncOpenAI
from tqdm import tqdm
from llm_output_parser import parse_json
from llmrunner import Runner, Task
from transformers import AutoTokenizer
import pandas as pd

from modules.data_template import CompetencyReportData
from modules.extractor import results_to_dataframe
from modules.vllm import get_model_name, llm_msg, clean_and_truncate_texts
from modules.validator import validate_competency_report_task


client = AsyncOpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1"
)

runner = Runner(
    client=client
)

MAX_TOKENS = 60000
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





with open("prompts/competence_extraction.md", "r") as f:
    prompt_template = f.read()

schema = CompetencyReportData.model_json_schema()
prompt_template = prompt_template.replace("{schema}", str(schema))

with open("output/competence_extraction.md", "w") as f:
    f.write(prompt_template) 



note = pd.read_feather("output/pdf_md_ocr.feather")


all_note = note.text.tolist()

texts = all_note[:10]
truncated_text = clean_and_truncate_texts(tokenizer, texts, MAX_TOKENS)

prompts = [prompt_template.replace("{report}", text) for text in truncated_text]
message_list = [llm_msg(prompt) for prompt in prompts]
tasks = [
    Task(messages=messages, 
         original = truncated_text[i],
         note_id = note.id[i]
         ) 
    for i, messages in enumerate(message_list)]


# timing
import time

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
df.to_feather("output/competence_extraction.feather")