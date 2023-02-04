from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seshapi.models import User, Session
from rest_framework.decorators import action
from rest_framework import generics


class SessionView(ViewSet):
  """Request Handlers for Sessions"""
  
  def retrieve(self, request, pk):
    try:
      session = Session.objects.get(pk=pk)
      serializer = SessionSerializer(session)
      
      return Response(serializer.data)
    except Session.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  
  def list(self, request):
    sessions = Session.objects.all()
    id_query = request.query_params.get('id', None)
    if id_query is not None:
      sessions = sessions.filter(session=id_query)
    serializer = SessionSerializer(sessions, many = True)
    return Response(serializer.data)

  def create(self, request):
    
    creator = User.objects.get(id=request.data["creator_id"])
    session = Session.objects.create(
      creator=creator,
      title=request.data["title"],
      session_image_url=request.data["session_image_url"],
      description=request.data["description"],
      address=request.data["address"],
      city=request.data["city"],
      state=request.data["state"],
      contest=request.data["contest"]
    )
    serializer = SessionSerializer(session)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """PUT requests for Sessions"""
    session = Session.objects.get(pk=pk)
    
    session.creator = request.data["creator"]
    session.title = request.data["title"]
    session.session_image_url = request.data["session_image_url"]
    session.description = request.data["description"]
    session.address = request.data["address"]
    session.city = request.data["city"]
    session.state = request.data["state"]
    session.contest = request.data["contest"]
    session.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    """DELETE session"""
    session = Session.objects.get(pk=pk)
    session.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = ('id','creator','title', 'session_image_url', 'description', 'address', 'city', 'state', 'contest') 
        depth = 1

class mySessionView(generics.ListCreateAPIView):
  serializer_class = SessionSerializer
  def get_queryset(self):
    creator_id = self.kwargs['creator_id']
    return Session.objects.filter(creator__id=creator_id)
