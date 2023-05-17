from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from review.models import Review

class CreateReviewSerializer(ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Review
        fields = ('content', 'rating', 'recipe', 'user_id')


class ReviewDetailSerializer(ModelSerializer):
    user_image = StringRelatedField(source='user.image.url', read_only=True)
    username = StringRelatedField(source='user.username', read_only=True)
    class Meta:
        model = Review
        fields = ('id','content','last_edited', 'rating', 'recipe', 'username','user_image')
