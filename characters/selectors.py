from django.db.models.query import QuerySet

from characters.filters import CharacterFilter
from characters.models import Character


def character_list(*, filters=None) -> QuerySet[Character]:
    filters = filters or {}

    qs = Character.objects.all()

    return CharacterFilter(filters, qs).qs
