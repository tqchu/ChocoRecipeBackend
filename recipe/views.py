from django.db.models import Avg, F, Count
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Ingredient, Recipe, FavoriteRecipe
from recipe.serializers import CreateRecipeSerializer, RecipeDetailSerializer, RecipeSerializer
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

        if (request.method == 'POST' or request.method == "PUT" or request.method == "DELETE") and not request.user.is_authenticated:
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

        recipes = result_set.annotate(average_rating=Avg('reviews__rating')).annotate(num_likes=Count('favoriterecipe')).order_by(sort_field)

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CreateRecipeSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            if user_id != request.user.id:
                return Response({'error': 'You are not authorized to create a recipe for another user.'},
                                status=status.HTTP_403_FORBIDDEN)

            recipe = Recipe.objects.create(
                user=request.user,
                title=serializer.validated_data.get('title'),
                directions=serializer.validated_data.get('directions'),
                calories=serializer.validated_data.get('calories'),
                cooking_time=serializer.validated_data.get('cooking_time'),
                image=serializer.validated_data.get('image')
            )

            # Create a list of ingredient objects and add them to the new recipe
            ingredients_data = serializer.validated_data.get('ingredients')
            for ingredient_data in ingredients_data:
                Ingredient.objects.create(
                    recipe=recipe,
                    name=ingredient_data.get('name'),
                    quantity=ingredient_data.get('quantity'),
                    unit=ingredient_data.get('unit')
                )

            serializer = CreateRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        id = request.data.get('id')
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response({'error': 'Recipe does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateRecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            if user_id != request.user.id:
                return Response({'error': 'You are not authorized to update a recipe for another user.'},
                                status=status.HTTP_403_FORBIDDEN)

            recipe = serializer.save()

            # Update the list of ingredient objects for the recipe
            Ingredient.objects.filter(recipe=recipe).delete()
            ingredients_data = serializer.validated_data.get('ingredients')
            for ingredient_data in ingredients_data:
                Ingredient.objects.create(
                    recipe=recipe,
                    name=ingredient_data.get('name'),
                    quantity=ingredient_data.get('quantity'),
                    unit=ingredient_data.get('unit')
                )

            serializer = CreateRecipeSerializer(recipe)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        id = request.data.get('id')
        user_id = request.data.get('user_id')
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response({'error': 'Recipe does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CreateRecipeSerializer(recipe)
        
        if user_id != request.user.id:
            return Response({'error': 'You are not authorized to update a recipe for another user.'},
                                status=status.HTTP_403_FORBIDDEN)
        serializer.delete(recipe)

        return Response(status=status.HTTP_204_NO_CONTENT)

class RecipeDetail(APIView):
    def get(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        recipe.author = recipe.user.username
        recipe.average_rating = recipe.reviews.aggregate(Avg('rating'))['rating__avg']
        recipe.num_likes = FavoriteRecipe.objects.filter(recipe=recipe).count()
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED
