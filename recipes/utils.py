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
                "content": "You are a recipe database that outputs only a list of recipe names.\n"
                           "You give at least 3 recipe names.\n"
                           "Ensure it includes only the name of the recipes:\n"
                           "DOn't number them"
            },
            {
                "role": "user",
                "content": f"Fetch a list of recipes for {recipe_name}",
            },
        ],
        model="llama3-8b-8192",
        temperature=0,
        stream=False,
        # response_format={"type": "json_array"},
    )


    # Extract the response content
    response_text = chat_completion.choices[0].message.content.strip()

    # Split the response into a list of recipe names
    recipe_names = response_text.split('\n')
    exclude_words = {'recipe', 'recipes', 'name', 'names', 'list', 'lists', 'title', 'titles'}

    # Filter out non-recipe lines (e.g., introduction lines)
    recipes = [line.strip() for line in recipe_names if line.strip() and not any(word in line.lower() for word in exclude_words)]


    # Format as a JSON response
    return JsonResponse({'recipes': recipes})

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
