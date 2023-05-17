from django.urls import path

from user.views import ChangePasswordView
from user.views import UserDetail
urlpatterns = [
    path('<int:pk>', UserDetail.as_view(), name='user_detail_view'),
    path('<int:pk>/change_password', ChangePasswordView.as_view(), name='change_password'),
]