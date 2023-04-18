from django.contrib.auth.models import update_last_login
from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

import djangoProject.settings as settings
class TokenSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user_id"] = str(self.user.id)
        # xem config
        update_last_login(None, self.user)

        return data


class MyTokenObtainPairSerializer(TokenSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        user_id = user.id
        # Add custom claims
        token['username'] = user.username
        return token
