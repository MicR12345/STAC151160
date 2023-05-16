from django.db import models

# Create your models here.
class Gatunek(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50, default='')

class Producent(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50,default='')

class Film(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=100,default='')
    rok = models.IntegerField()
    opis = models.TextField()
    producent = models.ForeignKey(Producent, on_delete=models.CASCADE,null=True)
    gatunki = models.ManyToManyField(Gatunek,null=True)
    owner = models.ForeignKey('auth.User', related_name='filmy', on_delete=models.CASCADE,null=True)
    class Meta:
        ordering = ['nazwa']

class Postac(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50,default='')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)






