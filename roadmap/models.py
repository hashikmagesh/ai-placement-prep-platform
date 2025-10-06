# from django.db import model

# Create your models here.
from django.db import models

class Topic(models.Model):
    domain = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    topic_name = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    order = models.IntegerField()