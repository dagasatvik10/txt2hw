from django.db.models.query import QuerySet

from characters.filters import CharacterFilter
from characters.models import Character
from users.models import BaseUser


def character_list(*, filters=None, user: BaseUser = None) -> QuerySet[Character]:
    filters = filters or {}

    qs = Character.objects.all()

    if user is not None:
        qs = qs.filter(user=user)

    return CharacterFilter(filters, qs).qs
