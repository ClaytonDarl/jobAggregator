from django.db import models
from rest_framework.authtoken.models import Token

# Create your models here.
class Posting(models.Model):
    title = models.CharField(max_length=100)
    salary = models.IntegerField()
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.title
