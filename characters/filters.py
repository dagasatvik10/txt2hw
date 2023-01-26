import django_filters

from characters.models import Character


class CharacterFilter(django_filters.FilterSet):
    upload_finished_at__isnull = django_filters.DateTimeFilter(field_name="upload_finished_at", lookup_expr="isnull")

    class Meta:
        model = Character
        fields = ("id", "value", "upload_finished_at", "user")

    @property
    def qs(self):
        parent = super().qs

        return parent.filter(upload_finished_at__isnull=False)
