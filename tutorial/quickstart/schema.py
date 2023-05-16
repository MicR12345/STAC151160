import graphene
from graphene import InputObjectType
from graphene_django import DjangoObjectType
from .models import *
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField


class FilmType(DjangoObjectType):
    class Meta:
        model = Film
        fields = ("id", "nazwa", "rok", "opis", "producent", "gatunki")

class FilmNode(DjangoObjectType):
    class Meta:
        model = Film
        filter_fields = {
            'nazwa': ['exact','contains','startswith'],
            'rok': ['exact']
        }
        interfaces = (relay.Node, )


class GatunekType(DjangoObjectType):
    class Meta:
        model = Gatunek
        fields = ("id","nazwa")

class ProducentType(DjangoObjectType):
    class Meta:
        model = Producent
        fields = ("id","nazwa")

class PostacType(DjangoObjectType):
    class Meta:
        model = Postac
        fields = ("id","nazwa","film")


class FilmUpdateMutationRelay(relay.ClientIDMutation):
    class Input:
        nazwa = graphene.String(required=True)
        id = graphene.ID()
        opis = graphene.String()
        rok = graphene.Int()
        producent = graphene.ID(default_value=None)
        gatunki = graphene.List(graphene.ID)

        film = graphene.Field(FilmType)

        @classmethod
        def mutate_and_get_payload(cls, root, info, nazwa, id, opis, rok, producent, gatunki):
            film = Film.objects.get(pk=id)
            film.opis = opis
            film.rok = rok
            film.producent = producent
            film.gatunki.set(gatunki)
            film.save()

            return FilmUpdateMutationRelay(film=film)






class FilmFilter(InputObjectType):
    nazwa_contains = graphene.String(default_value="")

class FilmCreateMutation(graphene.Mutation):
    class Arguments:
        nazwa = graphene.String(required=True)
        opis = graphene.String()
        rok = graphene.String()
        producent = graphene.ID(default_value=None)
        gatunki = graphene.List(graphene.ID)

    film = graphene.Field(FilmType)

    @classmethod
    def mutate(cls, root, info, nazwa, opis, rok, producent, gatunki):
        film = Film.objects.create(nazwa=nazwa, opis=opis, rok=rok, producent=producent)
        film.gatunki.set(gatunki)

        film.save()
        return FilmCreateMutation(film=film)


class FilmDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    film = graphene.List(FilmType)

    @classmethod
    def mutate(cls, root, info, id):
        film = Film.objects.get(pk=id).delete()
        film = Film.objects.all()
        return FilmCreateMutation(film=film)

class Query(graphene.ObjectType):
    filmy = DjangoFilterConnectionField(FilmNode)
    film_wg_id = relay.Node.Field(FilmNode)
    producent = graphene.List(ProducentType)
    producent_wg_id = graphene.Field(ProducentType, id = graphene.String())
    postacie = graphene.List(PostacType, nazwa_zawiera = graphene.String(default_value=""))
    gatunki = graphene.List(GatunekType, nazwa_zawiera=graphene.String(default_value=""))


    @staticmethod
    def resolve_producent(root, info):
        # We can easily optimize query count in the resolve method
        producent = Producent.objects.all()
        return producent


    @staticmethod
    def resolve_producent_wg_id(root, info, id):
        return Producent.objects.get(pk=id)

    @staticmethod
    def resolve_postacie(root, info, nazwa_zawiera):
        postac = Postac.objects.all()
        if nazwa_zawiera is not None:
            return Postac.objects.filter(nazwa__contains=nazwa_zawiera)
        return postac

    @staticmethod
    def resolve_gatunki(root, info, nazwa_zawiera):
        gatunek = Gatunek.objects.all()
        if nazwa_zawiera is not "":
            return Gatunek.objects.filter(film__nazwa__contains=nazwa_zawiera)
        return gatunek


class Mutation(graphene.ObjectType):
    update_film = FilmUpdateMutationRelay.Field()
    create_film = FilmCreateMutation.Field()
    delete_film = FilmDeleteMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)