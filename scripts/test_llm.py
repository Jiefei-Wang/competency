from pathlib import Path

from openai import AsyncOpenAI
import asyncio
from tqdm import tqdm
from llm_output_parser import parse_json
from transformers import AutoTokenizer
import pandas as pd

from modules.vllm import get_model_name, llm_msg, truncate_prompt


client = AsyncOpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1"
)
md_path = "output/pdf_md"

model_name = asyncio.run(get_model_name(client))
tokenizer = AutoTokenizer.from_pretrained(model_name)

MAX_TOKENS = 80000
MAX_CONCURRENCY = 128

async def indexed_llm(i, prompt, semaphore):
    async with semaphore:
        prompt = truncate_prompt(tokenizer, prompt, MAX_TOKENS)
        result = await llm_msg(client, prompt,
                               model_name=model_name)
    result_json = parse_json(result, strict=False)
    return i, result_json


async def async_extraction(prompts, max_concurrency=MAX_CONCURRENCY):
    semaphore = asyncio.Semaphore(max_concurrency)
    tasks = [
        asyncio.create_task(indexed_llm(i, prompt, semaphore))
        for i, prompt in enumerate(prompts)
    ]
    results = [None] * len(tasks)
    for fut in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Extracting"):
        i, res = await fut
        results[i] = res
    return results


with open("prompts/competence_extraction.txt", "r") as f:
    prompt_template = f.read()


# all md in md_path
md_files_all = list(Path(md_path).glob("*.md"))
md_files = md_files_all[:1000]  
# read all md files as text
all_text = []
for md_file in tqdm(md_files):
    text = md_file.read_text(encoding="utf-8")
    all_text.append(text)

df = pd.DataFrame({"name": [md_file.stem for md_file in md_files], "text": all_text})


# test_text = [note for note in all_note if "biopsy" in note]
texts = df["text"].tolist()[:100]
prompts = [prompt_template.replace("{report}", text) for text in texts]
extraction_results = asyncio.run(async_extraction(prompts))


# extraction_results is a list of dict, we can convert it to a dataframe
extracted_data = []
for res in extraction_results:
    if res is not None:
        extracted_data.append(res)

df_extracted = pd.DataFrame(extraction_results)
df_extracted["report_name"] = df["name"][:len(df_extracted)]
# move report_name to the first column
cols = df_extracted.columns.tolist()
cols = ["report_name"] + [col for col in cols if col != "report_name"]
df_extracted = df_extracted[cols]
df_extracted.to_excel("output/extracted_competence.xlsx", index=False)




