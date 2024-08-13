from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeIngredient, MealPlan, Review, Favourite

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Ingredient name cannot be empty.")
        return value

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be positive.")
        return value

    def validate_unit(self, value):
        if not value:
            raise serializers.ValidationError("Unit cannot be empty.")
        return value

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)

    class Meta:
        model = Recipe
        fields = '__all__'
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty")
        return value
    def validate_duplicate_ingredients(self, value):
        ingredients = value.get('ingredients')
        ingredient_names = []
        for ingredient in ingredients:
            if ingredient['ingredient']['name'] in ingredient_names:
                raise serializers.ValidationError("Duplicate ingredients are not allowed")
            ingredient_names.append(ingredient['ingredient']['name'])
        return value
    def validate_duplicate_recipe(self, value):
        if Recipe.objects.filter(name=value['name']).exists():
            raise serializers.ValidationError("Recipe already exists")
        return value

class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = '__all__'

    def validate(self, data):
        user_preferences = data['user'].dietary_preferences
        for recipe in data['recipes']:
            if not recipe.is_suitable_for(user_preferences):
                raise serializers.ValidationError(
                    f"{recipe.name} does not match your dietary preferences."
                )
        return data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']
        if Review.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("You have already reviewed this recipe.")
        return data

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']
        if Favourite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("You have already favorited this recipe.")
        return data
