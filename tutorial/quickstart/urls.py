from django.urls import path
from . import views

urlpatterns = [
    path('film/', views.FilmList.as_view(),name = views.FilmList.name),
    path('film/<int:pk>/',views.FilmDetail.as_view(), name = views.FilmDetail.name),
    path('postac/', views.PostacList.as_view(),name = views.PostacList.name),
    path('postac/<int:pk>/',views.PostacDetail.as_view(), name = views.PostacDetail.name),
    path('gatunek/', views.GatunekList.as_view(),name = views.GatunekList.name),
    path('gatunek/<int:pk>/',views.GatunekDetail.as_view(), name = views.GatunekDetail.name),
    path('producent/', views.ProducentList.as_view(),name = views.ProducentList.name),
    path('producent/<int:pk>/',views.ProducentDetail.as_view(), name = views.ProducentDetail.name),
    path('filmy/',views.film_list),
    path('filmy/<int:pk>',views.film_detail),
    path('gatunki/',views.gatunek_list),
    path('gatunki/<int:pk>',views.gatunek_detail),
    path('postacie/', views.postac_list),
    path('postacie/<int:pk>', views.postac_detail),
    path('producent2/', views.producent_list),
    path('producent2/<int:pk>', views.producent_detail),
]