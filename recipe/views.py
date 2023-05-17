from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from recipe.models import Recipe
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer


# Create your views here
#
#
#

def parse_sort_field(sort_field):
    sort_fields = {
        'rating': 'rating',
        'like': 'like',
        'calories': 'calories',
        'quick': 'cooking_time',
    }
    return sort_fields[sort_field]
class RecipeList(APIView):
    def get(self, request):
        params = request.query_params
        if 'sortBy' in params:
            sort_field = parse_sort_field(params['sortBy'])
        else:
            sort_field = 'id'
        recipes = Recipe.objects.all().order_by(sort_field)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

class RecipeDetail(APIView):
    def get(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED