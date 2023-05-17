from django.urls import path

from user.views import UserDetail

urlpatterns = [
    path('<int:pk>', UserDetail.as_view(), name='user_detail_view')
]