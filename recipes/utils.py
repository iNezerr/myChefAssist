# recipes/utils.py

import os
import json
from typing import List
from groq import Groq

from recipes.models import Recipe

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_recipe_from_groq(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the best expert recipe database that outputs recipes in JSON.\n"
                    "Ensure the JSON object includes the following fields:\n"
                    "- name: string\n"
                    "- description: string\n"
                    "- instructions: list of strings\n"
                    "- cook_time: integer (in minutes)\n"
                    "- prep_time: integer (in minutes)\n"
                    "- nutrition_facts: string\n"
                )
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",  # Specify your preferred model
        response_format={"type": "json_object"},
    )

    # Parse the response into a JSON object
    response_str = chat_completion.choices[0].message.content
    response_json = json.loads(response_str)

    return response_json

def get_recipe_variations(recipe_name: str) -> List[Recipe]:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a recipe database that outputs multiple variations of recipes in JSON.\n"
                f"The JSON array must use the schema: {json.dumps(Recipe.model_json_schema(), indent=2)}",
            },
            {
                "role": "user",
                "content": f"Fetch multiple variations for {recipe_name}",
            },
        ],
        model="llama3-8b-8192",
        temperature=0,
        stream=False,
        response_format={"type": "json_array"},
    )
    return [Recipe.model_validate_json(recipe) for recipe in chat_completion.choices[0].message.content]
