from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seshapi.models import User, Follow
from rest_framework.decorators import action
from rest_framework import generics

class FollowView(ViewSet):
  """handles all requests for follows"""
  def retrieve(self, request, pk):
    try:
      follow = Follow.objects.get(pk=pk)
      
      serializer = FollowSerializer(follow)
      return Response(serializer.data)
    
    except Follow.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
      
    
  
  def list(self, request):
    """handles GET requests for follows"""
    follows = Follow.objects.all()

    id_query = request.query_params.get('id', None)
    if id_query is not None:
      follows = follows.filte(id=id_query)
      
    serializer = FollowSerializer(follows, many=True)
    return Response(serializer.data)
    
  def destroy(self, request, pk):
    follow = Follow.objects.get(pk=pk)
    follow.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

  def create(self, request):
    """handles POST requests for follows"""
    follower = User.objects.get(pk=request.data['follower'])
    followed = User.objects.get(pk=request.data['followed'])

    follow = Follow.objects.create(
      follower = follower,
      followed = followed,
    )

    serializer = FollowSerializer(follow)
    return Response(serializer.data)
  
class FollowSerializer(serializers.ModelSerializer):

  class Meta:
    model = Follow
    fields =('id', 'follower', 'followed')
    depth = 2


class FollowerView(generics.ListCreateAPIView):
  serializer_class = FollowSerializer
  def get_queryset(self):
    follower_id = self.kwargs['follower_id']
    return Follow.objects.filter(follower__id=follower_id)
class FollowedView(generics.ListCreateAPIView):
  serializer_class = FollowSerializer
  def get_queryset(self):
    followed_id = self.kwargs['followed_id']
    return Follow.objects.filter(followed__id=followed_id)
