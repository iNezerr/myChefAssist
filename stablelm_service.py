import ollama
# 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
import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "what version are you?",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)
