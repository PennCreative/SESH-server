from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seshapi.models import User, Follow


class FollowView(ViewSet):
  """handles all requests for follows"""
  # def retrieve(self, request, pk):
  #   try:
  #     follow = Follow.objects.get(pk=pk)
  #   except:
  #     pass
    
  #   serializer = FollowSerializer(follow)
  #   return Response(serializer.data)
  
  def list(self, request):
    """handles GET requests for follows"""
    follows = Follow.objects.all()
    
    follower = request.query_params.get('follower', None)
    if follower is not None:
      follows = follows.filter(follower_id=follower)
      
    followed = request.query_params.get('followed', None)
    if followed is not None:
      follows = follows.filter(followed_id=followed)
      
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
      follow = followed,
    )

    serializer = FollowSerializer(follow)

    return Response(serializer.data)

class FollowSerializer(serializers.ModelSerializer):

  class Meta:
    model = Follow
    fields =('id', 'follower', 'followed')
    depth = 2
