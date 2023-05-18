from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipe.models import Recipe, Ingredient, FavoriteRecipe
from review.serializers import ReviewDetailSerializer


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name','quantity','unit', 'recipe')

class RecipeSerializer(ModelSerializer):
    author = serializers.CharField()
    average_rating = serializers.FloatField()
    num_likes = serializers.IntegerField()
    class Meta:
        model = Recipe
        fields = ('id','title','calories', 'cooking_time', 'image', 'average_rating', 'author', 'num_likes')


class RecipeDetailSerializer(RecipeSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    reviews = ReviewDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = ('id', 'title','ingredients', 'reviews','directions', 'calories', 'cooking_time', 'last_edited', 'image','average_rating', 'author','num_likes')


class CreateRecipeSerializer(RecipeSerializer):
    user_id = serializers.IntegerField()
    ingredients = IngredientSerializer(many=True,  read_only=True)
    class Meta:
        model = Recipe
        fields = ('id','user_id','title', 'directions', 'calories', 'cooking_time','image', 'ingredients')
        extra_kwargs = {
            'title': {'required': True},
            'directions': {'required': True},
            'calories': {'required': True},
        }

class FavoriteRecipeSerializer(ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ('id','user_id','recipe_id')
        extra_kwargs = {
            'id': {'read_only': True},
            'user_id': {'required': False}
        }