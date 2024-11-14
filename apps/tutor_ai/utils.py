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

def red_neuronal(user_message):
    # Crear el chat_completion con streaming habilitado
    is_red_neuronal = wrapper.chat.completions.create(
        model=MODEL,
        messages=get_messages(user_message),
        top_p=0.9,
        temperature=0.6,
        max_tokens=2000,
        stream=True,  # Habilitar streaming
        seed=None,
        frequency_penalty=None,
        presence_penalty=None,
    )
    return is_red_neuronal
