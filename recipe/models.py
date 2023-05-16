from django.db import models

from user.models import User


# Create your models here.
class Recipe(models.Model):
    # Many to One
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    directions = models.TextField()
    calories = models.IntegerField()
    cooking_time = models.IntegerField()
    last_edited = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/recipe/')
class Ingredient(models.Model):
    # Many to One
    recipe = models.ForeignKey(Recipe,related_name='ingredients' ,on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)

class FavoriteRecipe(models.Model):
    # Relation - model relationship django?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')
class Review(models.Model):
    # Many to One
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name="reviews",on_delete=models.CASCADE)
    content = models.TextField()
    last_edited = models.DateTimeField(auto_now=True)
    rating = models.IntegerField()
