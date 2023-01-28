from django.db import models
from .user import User
from .session import Session


class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="session")
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendee")
    
