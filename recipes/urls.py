from django.urls import path
from .views import *

urlpatterns = [
    path('ingredients/', IngredientList.as_view(), name='ingredient-list'),
    path('ingredients/<int:pk>', IngredientDetail.as_view(), name='ingredient-detail'),
    path('recipes/', RecipeList.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetail.as_view(), name='recipe-detail'),
    path('mealplans/', MealPlanList.as_view(), name='mealplan-list'),
    path('mealplans/<int:pk>/', MealPlanDetail.as_view(), name='mealplan-detail'),
    path('reviews/', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('favourites/', FavouriteList.as_view(), name='favourite-list'),
    path('favourites/<int:pk>', FavouriteDetail.as_view(), name='favourite-detail'),
    path('generate-recipe/', generate_recipe, name='generate-recipe'),
    path('search-recipe/', search_recipes, name='search-recipe'),
]
