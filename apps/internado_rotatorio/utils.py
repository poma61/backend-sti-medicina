
from .setup_ai import get_evaluation_questions, get_questions
import environ
import requests
import json

env = environ.Env()
environ.Env.read_env()
base_url = env("AI_BASE_URL")
access_token = env("AI_ACCESS_TOKEN")
MODEL = "tgi"


def red_neuronal(prompt,  top_p, temperature, max_tokens, seed, frequency_penalty=None, presence_penalty=None):
    #  si user_auth es None significa que es generacion de cuestionario
    if prompt.get("generate_questions"):
        is_message = get_questions(prompt.get("generate_questions"))
    else:
        is_message = get_evaluation_questions(prompt.get("evaluation_questions"))
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model":MODEL,
        "messages":is_message,
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




# from openai import OpenAI as WrapperAI
# wrapper = WrapperAI(
#     base_url=base_url,
#     api_key=access_token,
# )

# def red_neuronal(input,  top_p, temperature, max_tokens, stream, seed, frequency_penalty=None, presence_penalty=None):
#     #  si user_auth es None significa que es generacion de cuestionario
#     if input.get("generate_questions"):
#         is_message = get_questions(input.get("generate_questions"))
#     else:
#         is_message = get_evaluation_questions(input.get("evaluation_questions"))

#     is_red_neuronal = wrapper.chat.completions.create(
#         model=MODEL,
#         messages=is_message,
#         top_p=top_p,
#         temperature=temperature,
#         max_tokens=max_tokens,
#         stream=stream, 
#         seed=seed,
#         frequency_penalty=frequency_penalty,
#         presence_penalty=presence_penalty,
#     )

#     return is_red_neuronal



