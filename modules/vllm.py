import re
from modules.validator import validate_task
from llm_output_parser import parse_json

async def get_model_name(client):
    models = await client.models.list()
    model_name = models.data[0].id
    return model_name

def llm_msg(prompt):
    messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    return messages


def clean_text(text):
    if text is None:
        return ""
    text = str(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def truncate_prompts(tokenizer, prompts, max_tokens):
    encoded = tokenizer(
        prompts,
        add_special_tokens=False,
        truncation=True,
        max_length=max_tokens,
    )["input_ids"]
    return tokenizer.batch_decode(encoded)


def clean_and_truncate_texts(tokenizer, texts, max_tokens):
    cleaned_texts = [clean_text(text) for text in texts]
    return truncate_prompts(tokenizer, cleaned_texts, max_tokens)



def runner_json(task, data_template):
    ok, reasons, parsed_data = validate_task(task, data_template)
    if not ok and len(task.messages)<=6: # only retry twice (initial + 1 retry)
        validation_msg = "\n".join(reasons)
        print(f"task.index: {task.index}. Validation: {validation_msg}")
        task.messages.append({"role": "user", "content": validation_msg})
        return task

    return parsed_data
