import os
import json
from django.http import JsonResponse
from groq import Groq
from rest_framework import generics
from rest_framework.decorators import api_view
from .utils import get_recipe_from_groq, get_recipe_variations, suggest_recipes
from .models import Ingredient, Recipe, MealPlan, Review, Favourite, RecipeIngredient
from .serializers import IngredientSerializer, RecipeSerializer, MealPlanSerializer, ReviewSerializer, FavouriteSerializer


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


def generate_recipe(request):
    prompt = request.GET.get('prompt')
    if not prompt:
        return JsonResponse({'error': 'Prompt is required'}, status=400)

    response = get_recipe_from_groq(prompt)

    if response:
        return JsonResponse(response, safe=False)
    else:
        return JsonResponse({'error': 'Failed to get a response from the AI'}, status=500)

@api_view(['GET'])
def get_recipe_list(request):
    query = request.GET.get('q', '')
    if query:
        # Call the AI model to get multiple recipe variations
        suggested_recipes = suggest_recipes(query)
        return suggested_recipes
    else:
        return JsonResponse({'error': 'No query provided'}, status=400)


@api_view(['GET'])
def search_recipes(request):
    query = request.GET.get('q', '')
    if query:
        # Call the AI model to get multiple recipe variations
        suggested_recipes = get_recipe_variations(query)
        return JsonResponse({'results': [recipe.dict() for recipe in suggested_recipes]})
    else:
        return JsonResponse({'error': 'No query provided'}, status=400)
