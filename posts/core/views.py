from django.shortcuts import render
from rest_framework.views import APIView

from .serializers import PostSerializer
from .models import Post
from rest_framework.response import Response
import requests

# Create your views here.
class PostAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        #serializer = PostSerializer(posts, many=True)
        #return Response(serializer.data)
        return Response([self.formatPost(p)  for p in posts])

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def formatPost(self, post):
        comments = requests.get('http://localhost:8001/api/posts/%d/comments' % post.id).json()
        return {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            #'comments': []
            'comments': comments
        }