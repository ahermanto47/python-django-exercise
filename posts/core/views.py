from django.shortcuts import render
from rest_framework.views import APIView

from .serializers import PostSerializer
from .models import Post
from rest_framework.response import Response

# Create your views here.
class PostAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)