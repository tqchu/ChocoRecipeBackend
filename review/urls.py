from django.urls import path
from django.urls import path

from recipe.views import RecipeDetail, RecipeList
from review.views import ReviewList

urlpatterns = [
    path('', ReviewList.as_view(), name='review_detail_view')

]