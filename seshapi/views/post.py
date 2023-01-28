import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seshapi.models import Post, User
from rest_framework.decorators import action
from rest_framework import generics
class PostView(ViewSet):

    def retrieve(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        posts = Post.objects.all()
        id_query = request.query_params.get('id', None)
        if id_query is not None:
          posts = posts.filter(post=id_query)
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)

    def create(self, request):

        creator = User.objects.get(id=request.data["creator"])
        post = Post.objects.create(
            creator = creator,
            publication_date = request.data["publication_date"],
            content = request.data["content"]
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
        fields = ('id', 'creator', 'publication_date', 'content') 
        depth = 1

class myPostView(generics.ListCreateAPIView):
  serializer_class = PostSerializer
  def get_queryset(self):
    creator_id = self.kwargs['creator_id']
    return Post.objects.filter(creator__id=creator_id)
