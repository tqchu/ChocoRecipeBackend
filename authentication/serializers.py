from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from authentication.models import User


class LoginSerializer(serializers.ModelSerializer):
    # Override default constraint of username of User model -> exclude Unique constraint
    username = serializers.CharField(max_length=150)
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        username = self.initial_data['username']
        password = self.initial_data['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            if user.is_active:
                return {
                    "id": user.id}
            else:
                msg = 'User account is disabled.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user