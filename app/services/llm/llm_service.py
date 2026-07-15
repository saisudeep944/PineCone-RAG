from groq import Groq

from app.core.config import (
    GROQ_API_KEY
)

client = Groq(

    api_key=GROQ_API_KEY
)
def stream_answer(
    prompt
):

    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "user",

                "content": prompt
            }
        ],

        temperature=0,

        stream=True
    )

    for chunk in completion:

        delta = (
            chunk.choices[0]
            .delta.content
        )

        if delta:

            yield delta

def generate_answer(prompt):

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",

                "content":
                "You are a helpful "
                "enterprise AI assistant."
            },

            {
                "role": "user",

                "content": prompt
            }
        ],

        temperature=0
    )

    return (
        response
        .choices[0]
        .message.content
    )