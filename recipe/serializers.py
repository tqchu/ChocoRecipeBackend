from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipe.models import Recipe, Ingredient
from review.serializers import ReviewDetailSerializer


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name','quantity','unit')


class RecipeSerializer(ModelSerializer):
    author = serializers.CharField()
    average_rating = serializers.FloatField()
    class Meta:
        model = Recipe
        fields = ('id','title','calories', 'cooking_time', 'image', 'average_rating', 'author')


class RecipeDetailSerializer(RecipeSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    reviews = ReviewDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = ('id', 'title','ingredients', 'reviews','directions', 'calories', 'cooking_time', 'last_edited', 'image','average_rating', 'author')