from django.urls import path

from user.views import UserDetailView

urlpatterns = [
    path('<int:pk>', UserDetailView.as_view(), name='user_detail_view')
]