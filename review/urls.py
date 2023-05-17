from django.urls import path
from django.urls import path

from recipe.views import RecipeDetail, RecipeList
from review.views import ReviewList, ReviewDetail

urlpatterns = [
    path('', ReviewList.as_view(), name='review_detail_view'),
    path('<int:pk>', ReviewDetail.as_view(), name='review_detail_view')

]