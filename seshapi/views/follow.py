from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seshapi.models import User, Follow


class FollowView(ViewSet):
  """handles all requests for follows"""

  def list(self, request):
    """handles GET requests for follows"""
    follows = Follow.objects.all()

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
    
    depth: 2 
