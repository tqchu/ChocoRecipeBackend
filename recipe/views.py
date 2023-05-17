from django.db.models import Avg, F
from django.db.models import Q
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from recipe.models import Recipe
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer
from rest_framework import filters


# Create your views here
#
#
#

def parse_sort_field(sort_field):
    sort_fields = {
        'rating': '-average_rating',
        'like': '-like',
        'calories': '-calories',
        'quick': 'cooking_time',
    }
    return sort_fields[sort_field]


class RecipeList(APIView):
    def get(self, request):
        search = request.query_params.get('keyword')
        ordering = request.query_params.get('sortBy')
        if ordering:
            sort_field = parse_sort_field(ordering)
        else:
            sort_field = 'id'
        if search:
            recipes = Recipe.objects.annotate(
                author=F('user__username')
            ).filter(
                Q(directions__icontains=search) | Q(title__icontains=search) | Q(author__icontains=search)).annotate(
                average_rating=Avg('reviews__rating')).order_by(sort_field)
        else:
            recipes = Recipe.objects.annotate(
                author=F('user__username')
            ).annotate(average_rating=Avg('reviews__rating')).order_by(sort_field)

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)


class RecipeDetail(APIView):
    def get(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        recipe.average_rating = recipe.reviews.aggregate(Avg('rating'))['rating__avg']
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED
