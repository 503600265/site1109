import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
class Labeling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="labeling", null=True)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    publishDate = models.DateTimeField('date published', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = CloudinaryField('image', blank=True,null=True)

    # add images
    def __str__(self):
        return self.name
    def get_description(self):
        return self.description

    @admin.display(
        ordering='publish date',
        description='Publish Date',
    )
    def when_published(self):
        return self.publishDate
