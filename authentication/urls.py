"""account URL Configuration

The `urlpatterns` list routes URLs to views.
"""
from django.urls import path

from .apis import UserJwtLoginApi, UserJwtLogoutApi, UserMeAPI

app_name = "authentication"

urlpatterns = [
    path("login/", UserJwtLoginApi.as_view(), name="login"),
    path("logout/", UserJwtLogoutApi.as_view(), name="logout"),
    path("profile/", UserMeAPI.as_view(), name="profile"),
]
