import datetime
from django.db import models
from .user import User

class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateField(("Date"), default=datetime.date.today)    
    content = models.CharField(max_length=1000)
    approved = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
