from django.db import models
from .user import User

class Session(models.Model):

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    title = models.CharField(max_length=100)
    session_image_url = models.URLField(max_length=250)
    description = models.CharField(max_length=255)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=100)
    contest = models.BooleanField(default=True)
    
