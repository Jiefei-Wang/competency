

async def get_model_name(client):
    models = await client.models.list()
    model_name = models.data[0].id
    return model_name


async def llm_msg(client, prompt, model_name):
    resp = await client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    res = resp.choices[0].message.content
    return res


def truncate_prompt(tokenizer, prompt, max_tokens):
    tokens = tokenizer.encode(prompt)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens] 
    return tokenizer.decode(tokens)
