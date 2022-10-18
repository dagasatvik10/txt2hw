from django.urls import path

from .api import RegisterAPI, LoginAPI, UserAPI

app_name = 'user'

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path('login/', LoginAPI.as_view(), name='login'),
    path('profile/', UserAPI.as_view())
]
