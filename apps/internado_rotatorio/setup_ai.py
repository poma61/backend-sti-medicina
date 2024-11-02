def get_questions(generate_questions):
    tema = generate_questions["tema"]
    return [
        {
            "role": "system",
            "content": """ 
                        Eres un tutor en español especializado en medicina. Tu tarea es generar preguntas de un determinado tema de medicina.
                        Se te proporcionará, el tema, una breve introducción del tema y la cantidad de preguntas. Las preguntas deben ser complejas.
                        Solo debes generar preguntas de forma directa sin brindar ninguna introduccion ni informacion adicional. 
                        """,
        },
        {
            "role": "user",
            "content": f"""Tema: {tema.short_title}. 
                     Introducción del tema:{tema.contenido}.
                     Cantidad preguntas: 10 """,
        },
    ]


def get_evaluation_questions(evaluation_questions):
    user_auth = evaluation_questions["user_auth"]
    tema = evaluation_questions["tema"]
    questions = evaluation_questions["questions"]

    return [
        {
            "role": "system",
            "content": f"""Eres un tutor en español especializado en medicina. 
                        Tu tarea es evaluar el cuestionario del estudiante {user_auth.estudiante.nombres} {user_auth.estudiante.apellido_paterno} {user_auth.estudiante.apellido_materno}.
                        Se te proporcionara el tema, una breve introduccion del tema y el cuestionario con sus respectivas respuestas. 
                        Una vez terminado la revisión del cuestionario debes indicar que debe ir al menu del sistema, ir a la opcion TutorAI, para que
                        pueda realizar sus consultas de manera personalizada y pueda conversar contigo. 
                        """,
        },
        {
            "role": "user",
            "content": f""" Hola soy {user_auth.estudiante.nombres} {user_auth.estudiante.apellido_paterno} {user_auth.estudiante.apellido_materno}.
                        Te envio mi tema, breve introducción del tema y mi cuestionario para que puedas evaluarme.
                    Tema: {tema.short_title}. 
                     Introducción:{tema.contenido}.
                     cuestionario:
                     {questions}
                    """,
        },
    ]
