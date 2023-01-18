from django.db import models


class Session(models.Model):

    creator = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=100)
    datetime = models.DateField(auto_now=True)
    contest = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
