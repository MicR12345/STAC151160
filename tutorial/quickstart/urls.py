from django.urls import path
from . import views

urlpatterns = [
    path('film/', views.ClientList.as_view(),name = views.ClientList.name),
    path('film/<int:pk>/',views.ClientDetail.as_view(), name = views.ClientDetail.name),
]