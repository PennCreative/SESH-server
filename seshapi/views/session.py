from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seshapi.models import User, Session, Attendance

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
    attending = Attendance.objects.all()
    session
    
