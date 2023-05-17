from django.urls import path
from django.urls import path

from recipe.views import RecipeDetail, RecipeList

urlpatterns = [
    path('<int:pk>', RecipeDetail.as_view(), name='recipe_detail_view'),
    path('', RecipeList.as_view(), name='recipe_view')
]