from django.urls import include, path

urlpatterns = [path("auth/", include("account.urls", "account"))]
