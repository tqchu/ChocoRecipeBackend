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
    ingredients = IngredientSerializer(many=True)
    user_id = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id','user_id','title', 'directions', 'calories', 'cooking_time','image', 'ingredients')
        extra_kwargs = {
            'title': {'required': True},
            'directions': {'required': True},
            'calories': {'required': True}
        }

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)
        return recipe
    
    
    def update(self,instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.directions = validated_data.get('directions', instance.directions)
        instance.calories = validated_data.get('calories', instance.calories)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image',instance.image)

        ingredients_data = validated_data.get('ingredients')
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            if ingredient_id:
                # update existing ingredient
                ingredient = Ingredient.objects.get(id=ingredient_id)
                ingredient.name = ingredient_data.get('name', ingredient.name)
                ingredient.quantity = ingredient_data.get('quantity', ingredient.quantity)
                ingredient.unit = ingredient_data.get('unit', ingredient.unit)
                ingredient.save()
            else:
                # create new ingredient
                Ingredient.objects.create(recipe=instance, **ingredient_data)

        instance.save()
        return instance
    
    def delete(self,instance):
        instance.delete()
