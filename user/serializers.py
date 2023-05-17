from rest_framework.serializers import ModelSerializer
from rest_framework import serializers,status
from user.models import User
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
            model = User
            fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image']
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    current = serializers.CharField(max_length=150)
    password1 = serializers.CharField(max_length=150)
    password2 = serializers.CharField(max_length=150)
    class Meta:
        model = User
        fields = ('current', 'password1', 'password2')
        extra_kwargs = {
            'current': {'required': True},
            'password1': {'required': True},
            'password2': {'required': True},
        }

    def validate(self, attrs):
        pk = self.initial_data['id']
        user = User.objects.get(pk=pk)
        current = self.initial_data['current']
        password1 = self.initial_data['password1']
        password2 = self.initial_data['password2']
    
        if user.check_password(current):
            if password1 != password2:
                raise serializers.ValidationError({"password": "Password1 and password2 didn't match."})
        else :
            raise serializers.ValidationError({"password": "current password is not correct."}) 

        return attrs
    
    def update(self,instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        return instance