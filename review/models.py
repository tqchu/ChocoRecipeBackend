from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from recipe.models import Recipe
from user.models import User


# Create your models here.
class Review(models.Model):
    # Many to One
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name="reviews",on_delete=models.CASCADE)
    content = models.TextField()
    last_edited = models.DateTimeField(auto_now=True)
    rating = models.IntegerField( validators=[MinValueValidator(1), MaxValueValidator(5)])