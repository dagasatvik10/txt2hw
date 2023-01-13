from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("users/", include(("users.urls", "users"))),
    path("characters/", include("characters.urls", "characters")),
    path("auth/", include("authentication.urls", "authentication")),
]
