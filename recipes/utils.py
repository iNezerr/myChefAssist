# recipes/utils.py

import os
from os import getenv
import json
from typing import List
from django.http import JsonResponse
from groq import Groq
from dotenv import load_dotenv

from recipes.models import Recipe

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
                           "You give at least 4 recipe names.\n"
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
    print(selected_ingredients)
    if not isinstance(selected_ingredients, list):
        return {"error": "selected_ingredients should be a list."}

    # Convert the list of selected ingredients to a string
    selected_ingredients_str = "\n".join(selected_ingredients)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a culinary expert that refines a recipe based on the list of available ingredients.\n"
                    "You always update the recipe while keeping its core elements the same.\n"
                    "You will be given the original recipe and the ingredients available. \n"
                    "Check the differences between the original recipe and the ingredients available.\n"
                    "Use the ingredients available to give a MODIFIED version of the original recipe.\n"
                    "Use the original name of the recipe. Do not change it.\n"
                    "Use the available ingredients as the new ingredients. \n"
                    "You only refine the instructions, cook time, prep time, and nutrition facts if necessary.\n"
                    "And you output in JSON. \n"
                    "Ensure that the JSON object includes the following:\n"
                    "- name: string\n"
                    "- description: string\n"
                    "- ingredients: list of strings\n"
                    "- instructions: list of strings\n"
                    "- cook_time: integer (in minutes)\n"
                    "- prep_time: integer (in minutes)\n"
                    "- nutrition_facts: string\n"
                    # "Provide only this JSON object in your response, with no additional text and make sure all brackets that opened are closed when finished."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Original Recipe: {original_recipe}\n"
                    f"Available Ingredients:\n{selected_ingredients_str}\n"
                    "Refine the recipe based on these ingredients and provide the result in the exact JSON format specified above."
                )
            }
        ],
        model="llama3-8b-8192",
        temperature=0,
        stream=False,
        response_format={"type": "json_object"},
    )

    # Extract the response content
    refined_recipe_string = chat_completion.choices[0].message.content
    refined_recipe_str = json.loads(refined_recipe_string)
    return refined_recipe_str

    # Try parsing the response into a JSON object
    try:
        refined_recipe_json = json.loads(refined_recipe_str)
    except json.JSONDecodeError:
        return {"error": "Failed to parse the response from the AI model. Response may not be in JSON format."}

    return refined_recipe_json


