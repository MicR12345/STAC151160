import graphene
from datetime import datetime
from enum import Enum
from typing import Union
from graphql import GraphQLError

class ContactInfo:
    nazwa: str
    telefon: str
    def __init__(self,nazwa,telefon):
        self.nazwa = nazwa
        self.telefon = telefon

class AddressInfo:
    nazwa: str
    ulica: str
    miasto: str
    def __init__(self,ulica,miasto,nazwa = '',):
        self.nazwa = nazwa
        self.ulica = ulica
        self.miasto = miasto


class FilmState(Enum):
    AKTYWNY = "aktywny"
    NIEAKTYWNY = "nieaktywny"

class Film:
    tytul: str
    opis: str = None
    licencja_od: datetime = None
    licencja_do: datetime = None
    stan: FilmState = FilmState.AKTYWNY
    info: Union[AddressInfo, ContactInfo] = None
    def __init__(self,tytul,opis='',licencja_od=datetime.min,licencja_do=datetime.max,info = None):
        self.tytul = tytul
        self.opis = opis
        self.licencja_od = licencja_od
        self.licencja_do = licencja_do
        self.info = info

filmy = [
    Film(tytul="Ojciec chrzestny",
         opis="Saga rodziny Corleone",
         licencja_od=datetime.fromisoformat("2000-01-01T00:00"),
         licencja_do=datetime.fromisoformat("2025-12-31T23:59"),
         info = AddressInfo(nazwa="Agencja filmowa 'ORION'", ulica="Żeromskiego 14", miasto="Łódź"),
         ),
    Film(tytul="Interstellar",
         opis="Film science-fiction",
         licencja_od=datetime.fromisoformat("2020-01-01T00:00"),
         info = ContactInfo(nazwa="Kowalski", telefon="521 654 456"),
         ),
    Film(tytul="Pan Tadeusz",
         opis="Ekranizacja 'Pana Tadeusza' Andrzeja Wajdy",
         licencja_od=datetime.fromisoformat("2000-01-01T00:00"),
         licencja_do=datetime.fromisoformat("2025-12-31T23:59")
         ),
    Film(tytul="Pozegnanie z Afryką",
         opis="Romans/Dramat",
         licencja_od=datetime.fromisoformat("1985-01-01T00:00"),
         licencja_do=datetime.fromisoformat("2020-12-31T23:59")
         )
]
class FilmFilter(graphene.InputObjectType):
    tytul_zawiera = graphene.String(default_value="")
    licencja_po = graphene.DateTime(default_value=datetime.min)
    licencja_przed = graphene.DateTime(default_value=datetime.max)

class InfoType(graphene.Interface):
    nazwa = graphene.String()

    @classmethod
    def resolve_type(cls, instance, info):
        if instance is None:
            return None
        elif isinstance(instance, AddressInfo):
            return AddressInfoType
        elif isinstance(instance, ContactInfo):
            return ContactInfoType


class AddressInfoType(graphene.ObjectType):
    class Meta:
        interfaces = (InfoType,)

    ulica = graphene.String()
    miasto = graphene.String()


class ContactInfoType(graphene.ObjectType):
    class Meta:
        interfaces = (InfoType,)

    telefon = graphene.String()

class FilmType(graphene.ObjectType):
    tytul = graphene.String()
    opis = graphene.String()
    licencja_od = graphene.DateTime()
    licencja_do = graphene.DateTime()
    opis_krotki = graphene.String()
    po_licencji = graphene.Boolean()
    stan = graphene.Enum.from_enum(FilmState)()
    info = graphene.Field(InfoType)

    @staticmethod
    def resolve_opis_krotki(root, info):
        if not root.opis:
            return None
        elif len(root.opis) < 10:
            return root.opis
        else:
            return root.opis[:8] + "..."

    @staticmethod
    def resolve_po_licencji(root, info):
        if root.licencja_do is None:
            return False
        elif root.licencja_do <= datetime.now():
            return True
        else:
            return False

    @staticmethod
    def resolve_tytul(root, info):
        return root.tytul.upper()
class CreateFilm(graphene.Mutation):
    class Arguments:
        tytul = graphene.String(required=True)
        opis = graphene.String()
        licencja_od = graphene.DateTime(default_value=datetime.min)
        licencja_do = graphene.DateTime(default_value=datetime.max)

    success = graphene.Boolean(description="'True' gdy mutacja zakończy się powodzeniem",
                               deprecation_reason="Pole będzie usunięte w wersji 2.0 aplikacji")
    film = graphene.Field(FilmType)

    @staticmethod
    def mutate(root, info, tytul, opis, licencja_od, licencja_do):
        if licencja_od > licencja_do:
            raise GraphQLError('Data rozpoczęcia licencji starsza od daty końca licencji',
                               extensions={"error":"DATE_FROM_GREATER_THAN_DATE_TO_ERROR"})
        film = Film(
            tytul=tytul,
            opis=opis,
            licencja_od=licencja_od,
            licencja_do=licencja_do
        )
        filmy.append(film)
        return CreateFilm(success=True, film=film)

class ChangeFilmState(graphene.Mutation):
    class Arguments:
        idx = graphene.Int(required=True)
        stan = graphene.Enum.from_enum(FilmState)(required=True)

    film = graphene.Field(FilmType)

    @staticmethod
    def mutate(root, info, idx, stan):
        film = filmy[idx]
        film.stan = stan
        return ChangeFilmState(film=film)

class DeleteFilm(graphene.Mutation):
    class Arguments:
        idx = graphene.Int(required=True)

    filmy = graphene.List(FilmType)

    @staticmethod
    def mutate(root, info, idx):
        filmy.pop(idx)
        return DeleteFilm(filmy=filmy)

class Mutation(graphene.ObjectType):
    create_film = CreateFilm.Field(description="Dodawanie nowego filmu do bazy danych")
    change_film_state = ChangeFilmState.Field(description="Zmiana stanu filmu: 'AKTYWNY' bądź 'NIEAKTYWNY'")
    delete_film = DeleteFilm.Field(description="Usuwanie filmu z bazy danych")



class Query(graphene.ObjectType):
    filmy = graphene.List(FilmType, filters=FilmFilter())

    @staticmethod
    def resolve_filmy(root, info, filters):
        if info.context["admin"]:
            if filters is None:
                return filmy
            return [
                film for film in filmy if
                filters.tytul_zawiera in film.tytul and filters.licencja_po <= film.licencja_od <= filters.licencja_przed
            ]
        else:
            raise GraphQLError("Not Authorized")

schema = graphene.Schema(query=Query,mutation=Mutation,types=[AddressInfoType, ContactInfoType])

query1 = """
query {
    filmy (filters: {tytulZawiera:"a" licencjaPo:"2000-01-01T00:00"} ) {
        tytul
        opis
        licencjaOd
        licencjaDo
        opisKrotki
        poLicencji
        }
}
"""
result = schema.execute(query1, context={"admin":True})
print(result)
query = """
mutation {
    createFilm (tytul:"Nietykalni", opis:"Komedia") {
        success
        film {
            tytul
            opis
        }
    }
}
"""


result = schema.execute(query, context={"admin":True})
print(result)
for film in filmy:
    print(film.tytul)
query2 = """
query {
    opisy: filmy (filters: {} ) {
        tytul
        opis
        opisKrotki
        }
    licencje: filmy (filters: {} ) {
        tytul
        licencjaOd
        licencjaDo
        poLicencji
        }
}
"""
result = schema.execute(query, context={"admin":True})
print(result)

query = """
    query {
        filmy ( filters:{} ) {
            tytul
            stan
        }
}

"""
result = schema.execute(query, context={"admin":True})
print(result)

query = """
    mutation {
        changeFilmState (idx: 0, stan: NIEAKTYWNY) {
            film {
                tytul
                stan
            }
        }
    }

"""

result = schema.execute(query, context={"admin":True})
print(result)

query = """
    mutation {
        deleteFilm (idx: 0) {
            filmy {
                tytul
            }
        }
    }

"""
print([f.tytul for f in filmy])
result = schema.execute(query)
print(result)
print([f.tytul for f in filmy])


query = """
    query {
        filmy ( filters:{} ) {
            tytul
            info {
                __typename
                ... on AddressInfoType {
                    ulica
                    miasto
                }
                ... on ContactInfoType {
                    nazwa
                    telefon
                }
            }
        }
}
"""
result = schema.execute(query, context={"admin":True})
print(result)
query = """
    query {
        filmy ( filters:{} ) {
            tytul
            info {
                nazwa
                __typename
                ... on AddressInfoType {
                    ulica
                    miasto
                }
                ... on ContactInfoType {
                    telefon
                }
            }
        }
}

"""

result = schema.execute(query, context={"admin":True})
print(result)

query = """
mutation {
    createFilm (tytul:"Nietykalni", opis:"Komedia") {
        success
        film {
            tytul
            opis
        }
    }
}

"""

print([f.tytul for f in filmy])
result = schema.execute(query)
print(result)
print([f.tytul for f in filmy])

query = """
mutation {
    createFilm (title:"Nietykalni", opis:1974) {
        success
        film {
            tytul
            opis
        }
    }
}

"""

print([f.tytul for f in filmy])
result = schema.execute(query)
print(result)
print([f.tytul for f in filmy])

query = """
mutation {
    createFilm (tytul:"Nietykalni", opis:"Komedia", licencjaOd: "2025-12-31T00:00", licencjaDo:"2020-12-31T00:00") {
        success
        film {
            tytul
            opis
        }
    }
}

"""

result = schema.execute(query, context={"admin":True})
print(result)

print(schema)

query = """
    query {
        filmy ( filters:{} ) {
            tytul
            info {
                nazwa
                __typename
                ... on AddressInfoType {
                    ulica
                    miasto
                }
                ... on ContactInfoType {
                    telefon
                }
            }
        }
}

"""

result = schema.execute(query, context={"admin":False})
print(result)
