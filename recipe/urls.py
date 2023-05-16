from django.urls import path
from django.urls import path

from recipe.views import RecipeDetailView

urlpatterns = [
    path('<int:pk>', RecipeDetailView.as_view(), name='recipe_detail_view')
]