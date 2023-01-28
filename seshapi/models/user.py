from django.db import models


class User(models.Model):

    uid = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    handle = models.CharField(max_length=25)
    bio = models.CharField(max_length=100)
    profile_image_url = models.URLField(max_length=250)
    email = models.EmailField(max_length=254)
    created_on = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
