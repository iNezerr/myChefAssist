from rest_framework import generics
from .models import Ingredient, Recipe, MealPlan, Review, Favourite
from .serializers import IngredientSerializer, RecipeSerializer, MealPlanSerializer, ReviewSerializer, FavouriteSerializer

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
