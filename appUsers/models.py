from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    dietary_preferences = models.TextField(null=True, blank=True)

# Ingredient model
class Ingredient(models.Model):
    name = models.CharField(max_length=200, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

# Recipe model
class Recipe(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    instructions = models.TextField(null=True, blank=True)
    cook_time = models.IntegerField(null=True, blank=True)
    prep_time = models.IntegerField(null=True, blank=True)
    nutrition_facts = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Through model for Recipe and Ingredient many-to-many relationship
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=200, blank=True)

# Meal Plan model
class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.date}"

# Review model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.recipe.name} - {self.rating}"

# Favorite model
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - {self.recipe.name}"
