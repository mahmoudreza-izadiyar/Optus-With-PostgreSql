from django.db import models


class Cars(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='static/images/')
    binaryPhoto = models.BinaryField(blank=True)
