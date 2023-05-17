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
    rating = SerializerMethodField()
    author = StringRelatedField(source='user.username', read_only=True)
    class Meta:
        model = Recipe
        fields = ('id','title','calories', 'cooking_time', 'image', 'rating', 'author')

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            return total_rating / len(reviews)
        else:
            return None


class RecipeDetailSerializer(RecipeSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = ('id', 'title','ingredients', 'reviews','directions', 'calories', 'cooking_time', 'last_edited', 'image','rating', 'author')