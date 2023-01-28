from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seshapi.models import Comment, User, Post
from rest_framework.decorators import action
from rest_framework import generics

class CommentView(ViewSet):

  def retrieve(self, request, pk):
    try:
      comment = Comment.objects.get(pk=pk)
      serializer = CommentSerializer(comment)
      return Response(serializer.data)
    except Comment.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

  def list(self, request):
    comments = Comment.objects.all()
    post = self.request.query_params.get("post_id", None)
    if post is not None:
      comments = comments.filter(post_id=post).order_by('created_on')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

  def create(self, request):
    creator = User.objects.get(id=request.data["creator_id"])
    post = Post.objects.get(pk=request.data["post_id"])

    comment = Comment.objects.create(
      post=post,
      creator=creator,
      content=request.data["content"],
    )
    serializer = CommentSerializer(comment)
    return Response(serializer.data)

  def update(self, request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.content = request.data["content"]
    comment.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CommentSerializer(serializers.ModelSerializer):
  """serializer for comments"""
  class Meta:
    model = Comment
    depth = 1
    fields = ('id', 'post', 'creator', 'content', 'publication_date')

class PostCommentView(generics.ListCreateAPIView):
  serializer_class = CommentSerializer
  def get_queryset(self):
    post_id = self.kwargs['post_id']
    return Comment.objects.filter(post__id=post_id)
