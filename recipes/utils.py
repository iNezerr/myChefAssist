# recipes/utils.py

import os
import json
from typing import List
from django.http import JsonResponse
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
                    "- ingredients: list of strings\n"
                    "- instructions: list of strings\n"
                    "- cook_time: integer (in minutes)\n"
                    "- prep_time: integer (in minutes)\n"
                    "- nutrition_facts: string\n"
                    "Do not include any extraneous text or formatting like backticks or code blocks. "
                    "Output only valid JSON."
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

def suggest_recipes(recipe_name: str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the best expert recipe database that outputs a list of at least 3 recipes in JSON format.\n"
                    "Ensure the JSON object includes the following fields:\n"
                    "- 'id': int\n"
                    "- 'name': string\n"
                    "- 'description': string\n"
                    "Do not include any extraneous text or formatting like backticks or code blocks. "
                    "Output only valid JSON."
                ),
            },
            {
                "role": "user",
                "content": recipe_name
            }
        ],
        model="llama3-8b-8192",
        temperature=0,
        stream=False,
    )

    # Extract the response content
    response_text = chat_completion.choices[0].message.content.strip()

    try:
        # Convert the string response to a JSON object
        recipes_json = json.loads(response_text)

        # Ensure the response is a list of recipes
        if isinstance(recipes_json, list):
            return JsonResponse({'recipes': recipes_json})
        else:
            return JsonResponse({'error': 'Unexpected response format'}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Failed to parse JSON from AI response'}, status=500)


def refine_recipe_with_ingredients(original_recipe, selected_ingredients):
    chat_completion = client.chat.completions.create(
        messages= [
            {
                "role": "system",
                "content": "You are a culinary expert that can refine a recipe based on a list of selected ingredients.\n"
                "Adjust the recipe based on the available ingredients while keeping the core recipe the same.\n"
                "Only update the recipe name, instructions, cook time, prep time, and nutrition facts, if neccessary.\n"
            },
            {
                "role": "user",
                "content": {
                    f"Original Recipe:{original_recipe} \n"
                    f"Available Ingredients: {selected_ingredients}\n"
                    "Please refine the recipe according to the available ingredients."
                }
            }
        ],
        model="llama3-8b-8192",
        temperature=0,
        stream=False,
    )
    refined_recipe = chat_completion.choices[0].message.content
    return refined_recipe
