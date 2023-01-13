from django.urls import include, path

from .apis import (
    CharacterDirectUploadFinishApi,
    CharacterDirectUploadStartApi,
    CharacterListApi,
)

app_name = "characters"

urlpatterns = [
    path(
        "upload/",
        include(
            (
                [
                    path("start/", CharacterDirectUploadStartApi.as_view(), name="start"),
                    path("finish/", CharacterDirectUploadFinishApi.as_view(), name="finish"),
                ],
                "upload",
            )
        ),
    ),
    path("", CharacterListApi.as_view(), name="list"),
]
