from django.urls import path

from user.views import UserDetailView,ChangePasswordView

urlpatterns = [
    path('<int:pk>', UserDetailView.as_view(), name='user_detail_view'),
    path('<int:pk>/change_password', ChangePasswordView.as_view(), name='change_password'),
]