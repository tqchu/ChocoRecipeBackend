from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from review.models import Review

class ReviewDetailSerializer(ModelSerializer):
    user_image = StringRelatedField(source='user.image.url', read_only=True)
    username = StringRelatedField(source='user.username', read_only=True)
    class Meta:
        model = Review
        fields = ('id','content','last_edited', 'rating', 'recipe', 'username','user_image')


class CreateReviewSerializer(ReviewDetailSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Review
        fields = ('content', 'rating', 'recipe', 'user_id', 'id','last_edited' ,'username','user_image' )
        extra_kwargs = {
            'id': {'read_only': True},
            'last_edited': {'read_only': True},
            'username': {'read_only': True},
            'user_image': {'read_only': True}
        }

class UpdateReviewSerializer(ReviewDetailSerializer):
    class Meta:
        model = Review
        fields = ('content', 'rating', 'recipe', 'user_id', 'id','last_edited' ,'username','user_image' )
        extra_kwargs = {
            'user_id': {'read_only': True},
            'recipe': {'read_only': True},
            'last_edited': {'read_only': True},
            'username': {'read_only': True},
            'user_image': {'read_only': True}
        }