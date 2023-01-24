import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seshapi.models import Post, User

class PostView(ViewSet):

    def retrieve(self, request, pk):
        
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def list(self, request):

        posts = Post.objects.all()
        uid_query = request.query_params.get('uid', None)
        if uid_query is not None:
          posts = posts.filter(user=uid_query)
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)

    def create(self, request):

        creator = User.objects.get(uid=request.data["user"])

        post = Post.objects.create(
            publication_date = datetime.date.today(), # request.data["publication_date"],
            content = request.data["content"],
            creator = creator
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk):

        post = Post.objects.get(pk=pk)

        post.publication_date = request.data["publication_date"]
        post.content = request.data["content"]
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)  

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)    

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'user', 'publication_date', 'content') 
        depth = 1
