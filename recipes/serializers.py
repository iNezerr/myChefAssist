from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeIngredient, MealPlan, Review, Favourite

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'
