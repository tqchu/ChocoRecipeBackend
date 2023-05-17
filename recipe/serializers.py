from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer

from recipe.models import Recipe, Ingredient, Review


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name','quantity','unit')


class ReviewSerializer(ModelSerializer):
    username = StringRelatedField(source='user.username', read_only=True)
    user_image = StringRelatedField(source='user.image.url', read_only=True)
    class Meta:
        model = Review
        fields = ('id','content','last_edited', 'rating', 'recipe', 'username','user_image')

class RecipeSerializer(ModelSerializer):
    author = serializers.CharField()
    average_rating = serializers.FloatField()
    class Meta:
        model = Recipe
        fields = ('id','title','calories', 'cooking_time', 'image', 'average_rating', 'author')


class RecipeDetailSerializer(RecipeSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = ('id', 'title','ingredients', 'reviews','directions', 'calories', 'cooking_time', 'last_edited', 'image','average_rating', 'author')