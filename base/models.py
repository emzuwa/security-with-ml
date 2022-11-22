from django.db import models

# Create your models here.


class Tutorial(models.Model):
    filename = models.CharField(max_length=70, blank=False, default='')
    prediction = models.CharField(max_length=200,blank=False, default='')
    date = models.DateTimeField()
