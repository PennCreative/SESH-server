import datetime
from django.db import models
from .user import User
from .post import Post

class Comment(models.Model):

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    publication_date = models.DateField(("Date"), default=datetime.date.today)
    content = models.CharField(max_length=1000)
    
