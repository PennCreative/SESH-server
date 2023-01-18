from django.db import models
from .user import User

class Follow(models.Model):

    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    