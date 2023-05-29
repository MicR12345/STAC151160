from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from .views import *
from rest_framework.authtoken.models import Token
class FilmTests(APITestCase):
    def create_users(self):
        if len(User.objects.all()) == 0:
            User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        if len(User.objects.all()) == 1:
            User.objects.create_user('test', 'test@test.test', 'test')

    def post_film_without_login(self, nazwa,rok,opis):
        url = reverse(FilmList.name)
        data = {'nazwa': nazwa,'rok':rok,'opis':opis}
        response = self.client.post(url, data, format='json')
        return response

    def post_film(self, nazwa,rok,opis):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email='admin@example.com',
            password='testpass123',
        )
        token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse(FilmList.name)
        data = {'nazwa': nazwa,'rok':rok,'opis':opis}
        response = self.client.post(url, data, format='json')
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
        response_one = self.post_film_without_login(nazwa,rok,opis)
        assert response_one.status_code == status.HTTP_403_FORBIDDEN or status.HTTP_401_UNAUTHORIZED

    def test_post_movie(self):
        nazwa = 'test'
        rok = 32
        opis = 'a'
        response_one = self.post_film(nazwa,rok,opis)
        print(response_one.status_code)
        assert response_one.status_code == status.HTTP_201_CREATED

    def test_get_film_without_login(self):
        assert self.get_film_without_login().status_code == status.HTTP_200_OK

# Create your tests here.
