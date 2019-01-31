from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Recording(models.Model):
    cover = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100,null=True)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    instrument = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="created_recordings", null=True)
    players = models.ManyToManyField(User, related_name="played_recordings")
    spotify = models.CharField(max_length=1000, null=True)
    youtube = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)