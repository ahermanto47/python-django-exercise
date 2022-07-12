from pydoc import describe
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)