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
    path('select-recipe/', generate_recipe, name='select-recipe'),
    path('get-recipe-list/', get_recipe_list, name='get_recipe_list'),
    path('recipes/current/ingredients/', get_recipe_ingredients, name='get-recipe_ingredients'),
    path('recipes/finalize/', finalize_recipe, name='finalize-recipe'),
]
