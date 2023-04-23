from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)
from authentication.views import LoginView, RegisterView

urlpatterns = [
    path('login', LoginView.as_view(), name='login_view'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='register_view'),
    path('logout', TokenBlacklistView.as_view(), name='logout_view')
]