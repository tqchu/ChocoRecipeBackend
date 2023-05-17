from django.urls import path
from django.urls import path


from recipe.views import RecipeDetail, RecipeList, FavoriteRecipeList, FavoriteRecipeDetail

urlpatterns = [
    path('<int:pk>', RecipeDetail.as_view(), name='recipe_detail_view'),
    path('favorites/', FavoriteRecipeList.as_view(), name='favorite_recipe_view'),
    path('favorites/<int:pk>', FavoriteRecipeDetail.as_view(), name='favorite_recipe_detail_view'),
    path('', RecipeList.as_view(), name='recipe_view')
]