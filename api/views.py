from rest_framework.response import Response
from rest_framework.decorators import api_view

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
def getRecipes(request):
    return Response({'I am one recipe', 'I am another recipe'})
