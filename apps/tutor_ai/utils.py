from .setup_ai import get_messages
from openai import OpenAI as WrapperAI


def create_chat_completion(base_url, access_token, user_message):
    wrapper = WrapperAI(
        base_url=base_url,
        api_key=access_token,
    )

    # Crear el chat_completion con streaming habilitado
    chat_completion = wrapper.chat.completions.create(
        model="tgi",
        messages=get_messages(user_message),
        top_p=0.9,
        temperature=0.6,
        max_tokens=1500,
        stream=True,  # Habilitar streaming
        seed=None,
        frequency_penalty=None,
        presence_penalty=None,
    )
    return chat_completion
