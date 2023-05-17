from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from djangoProject import settings

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('users/', include('user.urls')),
    path('recipes/', include('recipe.urls')),
    path('reviews/', include('review.urls'))
]
