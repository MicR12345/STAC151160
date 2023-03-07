from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from .serializers import UserSerializer, GroupSerializer,FilmSerializer
from .models import Film
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClientList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    name = 'film-list'
    ordering_fields = ['nazwa']

class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    name = 'film-detail'

@csrf_exempt
def film_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        filmy = Film.objects.all()
        serializer = Film(filmy, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def film_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        filmy = Film.objects.get(pk=pk)
    except Film.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = FilmSerializer(filmy)
        return JsonResponse(serializer.data)