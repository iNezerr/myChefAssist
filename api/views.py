from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view

from recipes.ai_model import adjust_recipe, suggest_recipes
from recipes.models import Recipe

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/recipes/',
        '/api/recipes/<id>',
        '/api/recipes/create/',
        '/api/recipes/update/<id>',
        '/api/recipes/delete/<id>',
    ]
    return Response(routes)

@api_view(['GET'])
def testApi(request):
    context = {
        'request': request.GET.get(),
        'message': 'Working!',
    }
    return Response(context)

@api_view(['GET'])
def search_recipes(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if query:
            # Call the AI model to get recipe suggestions
            suggested_recipes = suggest_recipes(query)
            return JsonResponse({'results': suggested_recipes})
        else:
            return JsonResponse({'error': 'No query provided'}, status=400)

def get_recipe_details(request):
    try:
        recipe = Recipe.objects.all()
        recipe_data = {
            'name': recipe.name,
            'description': recipe.description,
            'ingredients': list(recipe.ingredients.values()),
            'instructions': recipe.instructions,
            'cook_time': recipe.cook_time,
            'prep_time': recipe.prep_time,
            'nutrition_facts': recipe.nutrition_facts,
        }
        return JsonResponse(recipe_data)
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)

# This view checks the user's available ingredients and adjusts the recipe or suggests alternatives.

def check_ingredients(request):
    if request.method == 'POST':
        data = request.json()
        recipe_id = data.get('recipe_id')
        available_ingredients = data.get('ingredients', [])

        try:
            recipe = Recipe.objects.get(id=recipe_id)
            adjusted_recipe = adjust_recipe(recipe, available_ingredients)
            return JsonResponse({'adjusted_recipe': adjusted_recipe})
        except Recipe.DoesNotExist:
            return JsonResponse({'error': 'Recipe not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def getRecipes(request):
    return Response({'I am one recipe', 'I am another recipe'})

@api_view(['POST'])
def recipe(request):
    context = {'all_data':request.POST.get(),'message':"Succesfully added Recipe"}
    return Response(context)
@api_view(['GET'])
def search_recipe(request):
    return Response

@api_view(['GET'])
def get_recipe_details(request):
    return
