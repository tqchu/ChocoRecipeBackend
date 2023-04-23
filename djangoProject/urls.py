from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from djangoProject import settings

urlpatterns = [
    path("admin", admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('api-authentication', include('rest_framework.urls'))
]
