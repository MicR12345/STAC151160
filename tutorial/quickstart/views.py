from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, GroupSerializer,FilmSerializer,ProducentSerializer,PostacSerializer,GatunekSerializer
from .models import Film,Producent,Gatunek,Postac
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
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

class FilmList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    name = 'film-list'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nazwa']
    ordering_fields = ['nazwa']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    name = 'film-detail'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProducentList(generics.ListCreateAPIView):
    queryset = Producent.objects.all()
    serializer_class = ProducentSerializer
    name = 'producent-list'
    ordering_fields = ['nazwa']

class ProducentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producent.objects.all()
    serializer_class = ProducentSerializer
    name = 'producent-detail'

class GatunekList(generics.ListCreateAPIView):
    queryset = Gatunek.objects.all()
    serializer_class = GatunekSerializer
    name = 'gatunek-list'
    ordering_fields = ['nazwa']

class GatunekDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gatunek.objects.all()
    serializer_class = GatunekSerializer
    name = 'gatunek-detail'

class PostacList(generics.ListCreateAPIView):
    queryset = Postac.objects.all()
    serializer_class = PostacSerializer
    name = 'postac-list'
    ordering_fields = ['nazwa']

class PostacDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Postac.objects.all()
    serializer_class = PostacSerializer
    name = 'postac-detail'


@csrf_exempt
def film_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        filmy = Film.objects.all()
        serializer = FilmSerializer(filmy, many=True)
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

@csrf_exempt
def producent_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        producenci = Producent.objects.all()
        serializer = ProducentSerializer(producenci, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def producent_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        producenci = Producent.objects.get(pk=pk)
    except Producent.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProducentSerializer(producenci)
        return JsonResponse(serializer.data)

@csrf_exempt
def gatunek_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        gatunki = Gatunek.objects.all()
        serializer = GatunekSerializer(gatunki, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def gatunek_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        gatunki = Gatunek.objects.get(pk=pk)
    except Gatunek.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GatunekSerializer(gatunki)
        return JsonResponse(serializer.data)

@csrf_exempt
def postac_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        postacie = Postac.objects.all()
        serializer = PostacSerializer(postacie, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def postac_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        postacie = Postac.objects.get(pk=pk)
    except Postac.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostacSerializer(postacie)
        return JsonResponse(serializer.data)

class FilmViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'filmy': reverse('film-list', request=request, format=format)
    })