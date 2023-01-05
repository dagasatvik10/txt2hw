from django.urls import path

from .apis import UserListApi

app_name = "user"

urlpatterns = [
    path("", UserListApi.as_view(), name="list"),
]
