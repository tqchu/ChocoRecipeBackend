from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from review.models import Review
from review.serializers import CreateReviewSerializer, UpdateReviewSerializer


# Create your views here.
class ReviewList(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CreateReviewSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            if user_id != request.user.id:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        review = Review.objects.get(pk=pk)
        serializer = UpdateReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            user_id = review.user_id
            if user_id != request.user.id:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = Review.objects.get(pk=pk)
        user_id = review.user_id
        if user_id != request.user.id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


