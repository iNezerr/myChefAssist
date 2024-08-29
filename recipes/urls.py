from django.urls import path
from .views import (
    generate_recipe,
    get_recipe_list,
    get_recipe_ingredients,
    finalize_recipe,
)

urlpatterns = [
    path('select-recipe/', generate_recipe, name='select-recipe'),
    path('get-recipe-list/', get_recipe_list, name='get_recipe_list'),
    path('recipes/current/ingredients/', get_recipe_ingredients, name='get-recipe_ingredients'),
    path('recipes/finalize/', finalize_recipe, name='finalize-recipe'),
]
