from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CommentSerializer
from rest_framework.response import Response
from .models import Comment

# Create your views here.
class CommentsAPIView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PostCommentAPIView(APIView):
    def get(self, _, pk=None):
        comment = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)