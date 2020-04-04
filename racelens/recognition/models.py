from django.contrib.auth.models import User
from django.db import models

import storage_backends


class Event(models.Model):
    event_name = models.CharField(max_length=36)
    poster = models.ImageField(storage=storage_backends.PublicMediaStorage())
    slug = models.SlugField(null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event_name)
    

class Photo(models.Model):
    imageId = models.CharField(max_length=36, default=None, blank=True, null=True)
    image = models.ImageField(storage=storage_backends.PublicMediaStorage())
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.imageId


class Selfie(models.Model):
    image = models.ImageField(storage=storage_backends.SelfieMediaStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photos = models.ManyToManyField('Photo')

    def __str__(self):
        return self.image.name
