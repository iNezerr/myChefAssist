from django.db import models
from appUsers.models import User

# Create your models here.

# Ingredient model
class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)

    def __str__(self):
        return self.name

# Recipe model
class Recipe(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    cook_time = models.IntegerField(null=True, blank=True)
    prep_time = models.IntegerField(null=True, blank=True)
    nutrition_facts = models.TextField(null=True, blank=True)
    ingredients = models.TextField()

    def __str__(self):
        return self.name

    def is_suitable_for(self, dietary_preferences):
        # Check if the recipe is suitable for the user's dietary preferences
        return True


                                                                                            # Through model for Recipe and Ingredient many-to-many relationship
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} for {self.recipe.name}"


# Meal Plan model
class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s plan for {self.date}"

# Review model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Review of {self.recipe.name} by {self.user.username}"

# Favorite model
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} favorited {self.recipe.name}"
