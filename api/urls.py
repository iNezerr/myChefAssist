from django.urls import path
from . import views

urlpatterns = [
  path('', views.getRoutes),
  path('search/', views.search_recipes, name='search_recipes'),
    path('recipe/<int:recipe_id>/', views.get_recipe_details, name='get_recipe_details'),
    path('check-ingredients/', views.check_ingredients, name='check_ingredients'),

]
