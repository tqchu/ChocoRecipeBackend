from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


# Create your models here.
class Ingredient(models.Model):
    # Ingredient
    # Recipe
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=40)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

# class User(models.Model):
#     username = models.CharField(max_length=100)
#     password =
class Example(models.Model):
    # Ingredient
    # Recipe
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=40)

    def __str__(self):
        return self.field1
    # class Meta:
    #     ordering = ['field1']


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']