from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from recipe.models import Recipe
from recipe.serializers import RecipeDetailSerializer


# Create your views here
#
#
#
# class RecipesView(APIView):
#     def get(self, request):
#         snippets = Recipe.objects.all()
#         serializer = RecipeSerializer(snippets, many=True)
#         return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED).

class RecipeDetailView(APIView):
    def get(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED