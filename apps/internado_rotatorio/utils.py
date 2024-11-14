from openai import OpenAI as WrapperAI
from .setup_ai import get_evaluation_questions, get_questions
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

def red_neuronal(generate_questions=None, evaluation_questions=None):
    #  si user_auth es None significa que es generacion de cuestionario
    if generate_questions is not None:
        is_message = get_questions(generate_questions)
    else:
        is_message = get_evaluation_questions(evaluation_questions)

    is_red_neuronal = wrapper.chat.completions.create(
        model=MODEL,
        messages=is_message,
        top_p=0.9,
        temperature=0.6,
        max_tokens=1500,
        stream=True,  # Habilitar streaming
        seed=None,
        frequency_penalty=None,
        presence_penalty=None,
    )

    return is_red_neuronal
