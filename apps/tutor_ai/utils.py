from .setup_ai import get_messages
from openai import OpenAI as WrapperAI
import environ
env = environ.Env()
environ.Env.read_env()
base_url = env("AI_BASE_URL")
access_token = env("AI_ACCESS_TOKEN")
MODEL = "tgi"
wrapper = WrapperAI(
    base_url=base_url,
    api_key=access_token,
)

def red_neuronal(input, top_p, temperature, max_tokens, stream, seed, frequency_penalty=None, presence_penalty=None):
    # Crear el chat_completion con streaming habilitado
    is_red_neuronal = wrapper.chat.completions.create(
        model=MODEL,
        messages=get_messages(input),
        top_p=top_p,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=stream,
        seed=seed,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return is_red_neuronal
