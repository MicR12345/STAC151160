import graphene
import datetime
class Film:
    tytul: str
    opis: str = None
    licencja_od: datetime = None
    licencja_do: datetime = None
    def __init__(self,tytul,opis='',licencja_od=datetime.datetime.min,licencja_do=datetime.datetime.max):
        self.tytul = tytul
        self.opis = opis
        self.licencja_od = licencja_od
        self.licencja_do = licencja_do

filmy = [
    Film(tytul="Ojciec chrzestny",
         opis="Saga rodziny Corleone",
         licencja_od=datetime.datetime.fromisoformat("2000-01-01T00:00"),
         licencja_do=datetime.datetime.fromisoformat("2025-12-31T23:59")
         ),
    Film(tytul="Interstellar",
         opis="Film science-fiction",
         licencja_od=datetime.datetime.fromisoformat("2020-01-01T00:00"),
         ),
    Film(tytul="Pan Tadeusz",
         opis="Ekranizacja 'Pana Tadeusza' Andrzeja Wajdy",
         licencja_od=datetime.datetime.fromisoformat("2000-01-01T00:00"),
         licencja_do=datetime.datetime.fromisoformat("2025-12-31T23:59")
         ),
    Film(tytul="Pozegnanie z Afryką",
         opis="Romans/Dramat",
         licencja_od=datetime.datetime.fromisoformat("1985-01-01T00:00"),
         licencja_do=datetime.datetime.fromisoformat("2020-12-31T23:59")
         )
]
class FilmFilter(graphene.InputObjectType):
    tytul_zawiera = graphene.String(default_value="")
    licencja_po = graphene.DateTime(default_value=datetime.datetime.min)
    licencja_przed = graphene.DateTime(default_value=datetime.datetime.max)


class FilmType(graphene.ObjectType):
    tytul = graphene.String()
    opis = graphene.String()
    licencja_od = graphene.DateTime()
    licencja_do = graphene.DateTime()
    opis_krotki = graphene.String()
    po_licencji = graphene.Boolean()

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
        elif root.licencja_do <= datetime.datetime.now():
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

    success = graphene.Boolean()
    film = graphene.Field(FilmType)

    @staticmethod
    def mutate(root, info, tytul, opis):
        film = Film(
            tytul=tytul,
            opis=opis,
        )
        filmy.append(film)
        return CreateFilm(success=True, film=film)


class Mutation(graphene.ObjectType):
    create_film = CreateFilm.Field()


class Query(graphene.ObjectType):
    filmy = graphene.List(FilmType, filters=FilmFilter())

    @staticmethod
    def resolve_filmy(root, info, filters):
        if filters is None:
            return filmy
        return [
            film for film in filmy if
            filters.tytul_zawiera in film.tytul and
            filters.licencja_po <= film.licencja_od <= filters.licencja_przed
        ]

schema = graphene.Schema(query=Query,mutation=Mutation)

query1 = """
query {
    filmy (filters: {tytulZawiera:"e" licencjaPo:"2000-01-01T00:00"} ) {
        tytul
        opis
        licencjaOd
        licencjaDo
        opisKrotki
        poLicencji
        }
}
"""
result = schema.execute(query1)
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


result = schema.execute(query)
print(result)
for film in filmy:
    print(film.tytul)
result = schema.execute(query1)
print(result)
