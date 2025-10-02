from .setup_ai import get_messages
import environ
import requests
import json

env = environ.Env()
environ.Env.read_env()

base_url = env("AI_BASE_URL")
access_token = env("AI_ACCESS_TOKEN")


MODEL = "tgi"

def red_neuronal(prompt, top_p, temperature, max_tokens, seed, frequency_penalty=None, presence_penalty=None):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model":MODEL,
        "messages":get_messages(prompt),
        "top_p":top_p,
        "temperature":temperature,
        "max_tokens":max_tokens,
        "stream":True,
        "seed":seed,
        "frequency_penalty":frequency_penalty,
        "presence_penalty":presence_penalty
    }

    response = requests.post(base_url, headers=headers, data=json.dumps(data), stream=True) 

    return response.iter_lines()


# from openai import OpenAI
# MODEL = "tgi"
# wrapper = OpenAI(
#     base_url=base_url,
#     api_key=access_token,
# )

# def red_neuronal(prompt, top_p, temperature, max_tokens, stream, seed, frequency_penalty=None, presence_penalty=None):
#     # Crear el chat_completion con streaming habilitado
#     is_red_neuronal = wrapper.chat.completions.create(
#         model=MODEL,
#         messages=get_messages(prompt),
#         top_p=top_p,
#         temperature=temperature,
#         max_tokens=max_tokens,
#         stream=stream,
#         seed=seed,
#         frequency_penalty=frequency_penalty,
#         presence_penalty=presence_penalty,
#     )
#     return is_red_neuronal

