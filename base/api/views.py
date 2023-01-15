from rest_framework.decorators import api_view
from rest_framework.response import Response



def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    
    return Response(routes, safe=False)