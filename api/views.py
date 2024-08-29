from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view

from recipes.ai_model import adjust_recipe, suggest_recipes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/select-recipe/',
        '/api/get-recipe-list/',
        '/api/recipes/current/ingredients/',
        '/api/recipes/finalize/',
    ]
    return Response(routes)

@api_view(['GET'])
def testApi(request):
    context = {
        'request': request.GET,
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

@api_view(['POST'])
def check_ingredients(request):
    if request.method == 'POST':
        data = request.data
        recipe_id = data.get('recipe_id')  # assuming this is needed for some future non-database processing
        available_ingredients = data.get('ingredients', [])

        # This is where you might call an AI function or another service
        adjusted_recipe = adjust_recipe(recipe_id, available_ingredients)  # Adjusted logic to reflect the non-database scenario
        return JsonResponse({'adjusted_recipe': adjusted_recipe})

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['GET'])
def getRecipes(request):
    return Response({'I am one recipe', 'I am another recipe'})

@api_view(['POST'])
def recipe(request):
    context = {'all_data': request.POST.get(), 'message': "Successfully added Recipe"}
    return Response(context)

@api_view(['GET'])
def search_recipe(request):
    return Response({'message': 'This is a placeholder for searching a recipe.'})

@api_view(['GET'])
def get_recipe_details(request):
    return Response({'message': 'This is a placeholder for getting recipe details.'})
