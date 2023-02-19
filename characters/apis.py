from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins import ApiAuthMixin
from api.pagination import LimitOffsetPagination, get_paginated_response
from characters.models import Character
from characters.selectors import character_list
from characters.services import CharacterDirectUploadService


class CharacterDirectUploadStartApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        value = serializers.CharField()
        image_name = serializers.CharField()
        image_type = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = CharacterDirectUploadService(request.user)
        presigned_data = service.start(**serializer.validated_data)

        return Response(data=presigned_data)


class CharacterDirectUploadFinishApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        character_id = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        character_id = serializer.validated_data["character_id"]

        character = get_object_or_404(Character, id=character_id)

        service = CharacterDirectUploadService(request.user)
        service.finish(character=character)

        return Response({"id": character.id})


class CharacterListApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        value = serializers.CharField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Character
            fields = ("id", "value", "url")

    def get(self, request, *args, **kwargs):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        characters = character_list(filters=filters_serializer.validated_data, user=request.user)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=characters,
            request=request,
            view=self,
        )
