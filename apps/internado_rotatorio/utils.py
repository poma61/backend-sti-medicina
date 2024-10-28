from openai import OpenAI as WrapperAI
from .setup_ai import get_evaluation, get_question


def create_chat_completion(
    base_url, access_token, tema=None, user_auth=None, question=None
):
    wrapper = WrapperAI(
        base_url=base_url,
        api_key=access_token,
    )
    #  si user_auth es None significa que es generacion de cuestionario
    if user_auth is None:
        is_message = get_question(tema)
    else:
        is_message = get_evaluation(user_auth, tema, question)

    # Crear el chat_completion con streaming habilitado
    chat_completion = wrapper.chat.completions.create(
        model="tgi",
        messages=is_message,
        top_p=0.9,
        temperature=0.6,
        max_tokens=1500,
        stream=True,  # Habilitar streaming
        seed=None,
        frequency_penalty=None,
        presence_penalty=None,
    )

    return chat_completion
