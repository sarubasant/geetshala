from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=100)
    lyrics= models.TextField()
    release_date = models.DateField (null=True,blank=True)
    is_published = models.BooleanField(default=False)