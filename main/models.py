from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class file_record(models.Model):
    file_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255, null=True)
    link = models.URLField(max_length=255, null=True)
    enable_post = models.BooleanField(default=True)
