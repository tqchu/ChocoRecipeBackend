import json

from django.db.models import Avg, F, Count
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Ingredient, Recipe, FavoriteRecipe
from recipe.serializers import CreateRecipeSerializer, RecipeDetailSerializer, RecipeSerializer, \
    FavoriteRecipeSerializer, IngredientSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import PermissionDenied


# Create your views here
#
#
#

def parse_sort_field(sort_field):
    sort_fields = {
        'rating': '-average_rating',
        'like': '-num_likes',
        'calories': '-calories',
        'quick': 'cooking_time',
    }
    return sort_fields[sort_field]


class RecipeList(APIView):
    def check_permissions(self, request):

        if (
                request.method == 'POST' or request.method == "PUT" or request.method == "DELETE") and not request.user.is_authenticated:
            raise PermissionDenied()
        super().check_permissions(request)

    def get(self, request):
        search = request.query_params.get('keyword')
        ordering = request.query_params.get('sort_by')
        user_id = request.query_params.get('user_id')
        result_set = Recipe.objects
        # Annotate username and filter by user_id if needed
        if user_id:
            result_set = result_set.filter(
                user_id=user_id)
        # Parse sorting
        if ordering:
            sort_field = parse_sort_field(ordering)
        else:
            sort_field = 'id'
        # Search or not, we must annotate username to author first =))
        result_set = result_set.annotate(author=F('user__username'))
        # Searching
        if search:
            result_set = result_set.filter(
                Q(title__icontains=search) | Q(author__icontains=search))

        recipes = result_set.annotate(average_rating=Avg('reviews__rating')).annotate(
            num_likes=Count('favoriterecipe')).order_by(sort_field)

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        recipe_serializer = CreateRecipeSerializer(data=request.data)
        ingredient_serializer = IngredientSerializer(data=json.loads(request.data.get('ingredients')), many=True)
        if recipe_serializer.is_valid() and ingredient_serializer.is_valid():
            user_id = recipe_serializer.validated_data.get('user_id')
            if user_id != request.user.id:
                return Response({'error': 'You are not authorized to create a recipe for another user.'},
                                status=status.HTTP_403_FORBIDDEN)
            recipe = recipe_serializer.save()
            for ingredient in ingredient_serializer.validated_data:
                ingredient['recipe'] = recipe
            ingredient_serializer.save()
            recipe_serializer.data['ingredients'] = ingredient_serializer.data
            return Response(recipe_serializer.data, status=status.HTTP_201_CREATED)
        return Response(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        id = request.data.get('id')
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response({'error': 'Recipe does not exist'}, status=status.HTTP_404_NOT_FOUND)

        recipe_serializer = CreateRecipeSerializer(recipe, data=request.data)
        ingredient_serializer = IngredientSerializer(data=json.loads(request.data.get('ingredients')), many=True)

        if recipe_serializer.is_valid() and ingredient_serializer.is_valid():
            user_id = recipe_serializer.validated_data.get('user_id')
            if user_id != request.user.id:
                return Response({'error': 'You are not authorized to update a recipe for another user.'},
                                status=status.HTTP_403_FORBIDDEN)

            recipe = recipe_serializer.save()

            # Update the list of ingredient objects for the recipe
            Ingredient.objects.filter(recipe=recipe).delete()
            for ingredient in ingredient_serializer.validated_data:
                ingredient['recipe'] = recipe
            ingredient_serializer.save()
            recipe_serializer.data['ingredients'] = ingredient_serializer.data
            return Response(recipe_serializer.data, status= status.HTTP_200_OK)
        return Response(recipe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetail(APIView):
    def check_permissions(self, request):

        if (
                request.method == 'POST' or request.method == "PUT" or request.method == "DELETE") and not request.user.is_authenticated:
            raise PermissionDenied()
        super().check_permissions(request)
    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(id=pk)
        except Recipe.DoesNotExist:
            return Response({'error': 'Recipe does not exist'}, status=status.HTTP_404_NOT_FOUND)
        recipe.author = recipe.user.username
        recipe.average_rating = recipe.reviews.aggregate(Avg('rating'))['rating__avg']
        recipe.num_likes = FavoriteRecipe.objects.filter(recipe=recipe).count()
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response({'error': 'Recipe does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if recipe.user.id != request.user.id:
            return Response({'error': 'You are not authorized to update a recipe for another user.'},
                            status=status.HTTP_403_FORBIDDEN)
        recipe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class FavoriteRecipeList(APIView):
    permission_classes = [IsAuthenticated]

    def check_permissions(self, request):

        if (
                request.method == 'POST' or request.method == "PUT" or request.method == "DELETE") and not request.user.is_authenticated:
            raise PermissionDenied()
        super().check_permissions(request)

    def get(self, request):
        search = request.query_params.get('keyword')
        ordering = request.query_params.get('sort_by')
        result_set = Recipe.objects.filter(favoriterecipe__user=request.user)
        # Parse sorting
        if ordering:
            sort_field = parse_sort_field(ordering)
        else:
            sort_field = 'id'
        # Search or not, we must annotate username to author first =))
        result_set = result_set.annotate(author=F('user__username'))
        # Searching
        if search:
            result_set = result_set.filter(
                Q(title__icontains=search) | Q(author__icontains=search))

        recipes = result_set.annotate(average_rating=Avg('reviews__rating')).annotate(
            num_likes=Count('favoriterecipe')).order_by(sort_field)

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteRecipeSerializer(request.user, data=request.data)

        if serializer.is_valid():
            try:
                recipe = Recipe.objects.get(pk=request.data.get('recipe_id'))
            except Recipe.DoesNotExist:
                return Response({'error': 'Invalid recipe_id'}, status=status.HTTP_400_BAD_REQUEST)
            favorite_recipe = FavoriteRecipe()
            favorite_recipe.user = request.user
            favorite_recipe.recipe = recipe
            favorite_recipe.save()
            return Response({
                'id': favorite_recipe.id,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteRecipeDetail(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        favorite_recipe = FavoriteRecipe.objects.get(pk=pk)
        user_id = favorite_recipe.user_id
        if user_id != request.user.id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
