from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from .views import *
class FilmTests(APITestCase):
    def create_users(self):
        if len(User.objects.all()) == 0:
            User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        if len(User.objects.all()) == 1:
            User.objects.create_user('test', 'test@test.test', 'test')

    def post_film_without_login(self, nazwa,rok,opis,producent,gatunki):
        url = reverse(FilmList.name)
        data = {'nazwa': nazwa,'rok':rok,'opis':opis,'producent':producent,'gatunki':gatunki}
        response = self.client.post(url, data, format='json')
        return response

    def post_film(self, nazwa,rok,opis,producent):
        client = APIClient()
        client.force_login(User.objects.get_or_create(username='testuser')[0])
        url = reverse(FilmList.name)
        data = {'nazwa': nazwa,'rok':rok,'opis':opis,'producent':producent}
        client.request()
        response = client.post(url, data, format='json')
        return response

    def get_film_without_login(self):
        client = APIClient()
        url = reverse(FilmList.name)
        response = client.get(url, format='json')
        return response

    def test_post_filmie_without_login(self):
        nazwa = 'test'
        rok = 32
        opis = 'a'
        producent = 1
        gatunki = 1
        response_one = self.post_film_without_login(nazwa,rok,opis,producent,gatunki)
        assert response_one.status_code == status.HTTP_403_FORBIDDEN or status.HTTP_401_UNAUTHORIZED

    def test_post_movie(self):
        nazwa = 'test'
        rok = 32
        opis = 'a'
        producent = 1
        response_one = self.post_film(nazwa,rok,opis,producent)
        print(response_one.status_code)
        assert response_one.status_code == status.HTTP_201_CREATED

    def test_get_film_without_login(self):
        assert self.get_film_without_login().status_code == status.HTTP_200_OK

# Create your tests here.
