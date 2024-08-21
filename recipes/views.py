import os
import json
from django.http import JsonResponse
from groq import Groq
from rest_framework import generics
from rest_framework.decorators import api_view
from .utils import get_recipe_from_groq, get_recipe_variations, refine_recipe_with_ingredients, suggest_recipes
from .models import Ingredient, Recipe, MealPlan, Review, Favourite, RecipeIngredient
from .serializers import IngredientSerializer, RecipeSerializer, MealPlanSerializer, ReviewSerializer, FavouriteSerializer
from .cache_service import save_recipe_in_cache, get_recipe_from_cache



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

class IngredientList(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class IngredientDetail(generics.RetrieveAPIView):
  queryset = Ingredient.objects.all()
  serializer_class = IngredientSerializer

class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeDetail(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class MealPlanList(generics.ListCreateAPIView):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer

class MealPlanDetail(generics.RetrieveAPIView):
  queryset = MealPlan.objects.all()
  serializer_class = MealPlanSerializer

class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetail(generics.RetrieveAPIView):
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer

class FavouriteList(generics.ListCreateAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

class FavouriteDetail(generics.RetrieveAPIView):
  queryset = Favourite.objects.all()
  serializer_class = FavouriteSerializer

@api_view(['GET'])
def get_recipe_list(request):
    query = request.GET.get('q', '')
    if query:
        # Call the AI model to get multiple recipe variations
        suggested_recipes = suggest_recipes(query)
        return suggested_recipes
    else:
        return JsonResponse({'error': 'No query provided'}, status=400)

@api_view(['POST'])
def generate_recipe(request):
    prompt = request.POST.get('prompt')
    if not prompt:
        return JsonResponse({'error': 'Prompt is required'}, status=400)
    response = get_recipe_from_groq(prompt)

    if response:
        save_recipe(response)
        return JsonResponse(response, safe=False)
    else:
        return JsonResponse({'error': 'Failed to get a response from the AI'}, status=500)

def save_recipe(recipe):
    return save_recipe_in_cache('current_recipe', recipe)

def get_recipe_ingredients(request):
    cached_recipe = get_recipe_from_cache()

    if not cached_recipe:
        return JsonResponse({"error":"Recipe not found in chache"}, status=404)
    ingredients = cached_recipe.get('ingredients', [])
    recipe_name = cached_recipe.get('name', 'Recipe')
    context = {
            'recipe_name': recipe_name,
            'ingredients': ingredients
        }
    return JsonResponse(context)

@api_view(['POST'])
def finalize_recipe(request):
    selected_ingredients = request.data.get('selected_ingredients', [])
    original_recipe = get_recipe_from_cache()
    print(selected_ingredients)

    if not original_recipe:
        return JsonResponse({"error":"Recipe not found in chache"}, status=404)
    refined_recipe = refine_recipe_with_ingredients(original_recipe, selected_ingredients)
    if not refined_recipe:
        return JsonResponse({"error":"Failed to refine recipe"}, status=500)
    return JsonResponse({"refined_recipe": refined_recipe}, safe=False)


def save_recipe_to_DB(request):
    # Retrieve the cached recipe
    cached_recipe = get_recipe_from_cache()

    if cached_recipe:
        # Create a new Recipe object and save it to the database
        recipe = Recipe(
            name=cached_recipe.get('name'),
            description=cached_recipe.get('description'),
            instructions=cached_recipe.get('instructions'),
            cook_time=cached_recipe.get('cook_time'),
            prep_time=cached_recipe.get('prep_time'),
            nutrition_facts=cached_recipe.get('nutrition_facts'),
            ingredients=cached_recipe.get('ingredients')
        )
        recipe.save()

        return JsonResponse({'message': 'Recipe saved successfully.'})
    else:
        return JsonResponse({'error': 'No recipe found in cache.'}, status=400)
