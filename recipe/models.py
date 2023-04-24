from django.db import models

from user.models import User

class Ingredient(models.Model):
    # Relation with recipe
    # recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=255)
# Create your models here.
class Recipe(models.Model):
    # Relation - model relationship django?
    # Many to One
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    directions = models.TextField()
    calories = models.IntegerField()
    cooking_time = models.IntegerField()
    last_edited = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/recipe/')
class FavoriteRecipe(models.Model):
    # Relation - model relationship django?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
class Review(models.Model):
    # Relation - model relationship django?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField()
    last_edited = models.DateTimeField(auto_now=True)
    rating = models.IntegerField()
