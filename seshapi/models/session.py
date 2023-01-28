from django.db import models
from .user import User

class Session(models.Model):

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=100)
    datetime = models.DateField(auto_now=True)
    contest = models.BooleanField(default=True)
    
