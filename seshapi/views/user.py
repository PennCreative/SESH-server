"""View module for handling requests about users"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seshapi.models import User, Session
from rest_framework.decorators import action
from rest_framework import generics

class UserView(ViewSet):
  """SESH User View"""
  
  def retrieve(self, request, pk):
    """Handle GET single user"""
    try:
      user = User.objects.get(pk=pk)
      serializer = UserSerializer(user)
      return Response(serializer.data)
    
    except User.DoesNotExist as exception:
      return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)

  def list(self, request):
    """Handle GET requests to get all users"""
    users = User.objects.all()
    uid_query = request.query_params.get('uid', None)
    if uid_query is not None:
      users = users.filter(uid=uid_query)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
  
  def create(self, request):

        user = User.objects.create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            bio=request.data["bio"],
            city=request.data["city"],
            state=request.data["state"],
            ride=request.data["ride"],
            profile_image_url=request.data["profile_image_url"],
            email=request.data["email"],
            created_on=request.data["created_on"],
            active=request.data["active"],
            is_staff=request.data["is_staff"],
            uid=request.data["uid"],
        )
        serializer = UserSerializer(user)
        return Response(serializer.data)

  def update(self, request, pk):
    """Handle PUT requests for users
    Returns:
        Response -- Empty body with 204 status code
    """

    user = User.objects.get(pk=pk)
    
    user.uid = request.data["uid"]
    user.first_name = request.data["first_name"]
    user.last_name = request.data["last_name"]
    user.handle = request.data["handle"]
    user.ride = request.data["ride"]
    user.bio = request.data["bio"]
    user.city = request.data["city"]
    user.state = request.data["state"]
    user.profile_image_url = request.data["profile_image_url"]
    user.email = request.data["email"]
    user.active = request.data["active"]
    user.is_staff = request.data["is_staff"]
    user.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)

  def destroy(self, request, pk):
    """DELETE user"""
    user = User.objects.get(pk=pk)
    user.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
  """JSON serializer for Users"""
  class Meta:
    model = User
    fields = ('id', 'uid', 'first_name', 'last_name', 'handle', 'ride', 'bio', 'city', 'state', 'profile_image_url', 'email', 'created_on', 'active', 'is_staff')
      
class mySessionView(generics.ListCreateAPIView):
  serializer_class = UserSerializer
  def get_queryset(self):
    creator_id = self.kwargs['creator_id']
    return Session.objects.filter(creator__id=creator_id)
