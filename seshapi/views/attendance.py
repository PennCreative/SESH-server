from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from seshapi.models import User, Attendance, Session

class AttendanceView(ViewSet):
  """Requests for Attendance"""
  def retrieve(self, request, pk):
    try:
      attendance = Attendance.objects.get(pk=pk)
      serializer = AttendanceSerializer(attendance)
      return Response(serializer.data)
    except Attendance.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  def list(self, request):
    """GET requests for Attendance"""
    attending = Attendance.objects.all()
    session = self.request.query_params.get('session_id', None)
    
    if session is not None:
      attending = attending.filter(session_id=session)

    serializer = AttendanceSerializer(attending, many=True)
    return Response(serializer.data)
  
  def destroy(self, request, pk):
    attending = Attendance.objects.get(pk=pk)
    attending.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def create(self, request):
    """Handles POST"""
    
    attendee = User.objects.get(pk=request.data['attendee'])
    session = Session.objects.get(pk=request.data['session'])
    
    attendance = Attendance.objects.create(
      attendee = attendee,
      session = session
    )
    
    serializer = AttendanceSerializer(attendance)
    
    return Response(serializer.data)
  
class AttendanceSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Attendance
    fields = ('id', 'session', 'attendee')
