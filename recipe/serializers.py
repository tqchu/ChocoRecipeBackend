from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer

from recipe.models import Recipe, Ingredient, Review


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name','quantity','unit')


class ReviewSerializer(ModelSerializer):
    username = StringRelatedField(source='user.username', read_only=True)
    class Meta:
        model = Review
        fields = ('id','content','last_edited', 'rating', 'recipe', 'username')

class RecipeDetailSerializer(ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = ('title','ingredients', 'reviews','directions', 'calories', 'cooking_time', 'last_edited', 'image')
