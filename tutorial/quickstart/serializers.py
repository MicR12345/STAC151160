from django.contrib.auth.models import User, Group
from quickstart.models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    filmy = filmy = serializers.HyperlinkedRelatedField(many=True, view_name='film-detail', read_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups','filmy']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProducentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producent
        fields = ['id', 'nazwa']

class GatunekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gatunek
        fields = ['id', 'nazwa']

class PostacSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postac
        fields = ['id', 'nazwa','film']

class FilmSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Film
        fields = ['id', 'nazwa', 'rok', 'opis','producent','gatunki','owner']