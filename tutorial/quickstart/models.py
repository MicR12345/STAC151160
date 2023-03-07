from django.db import models

# Create your models here.

class Film(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=100,default='')
    rok = models.IntegerField()
    opis = models.TextField()

    class Meta:
        ordering = ['nazwa']
