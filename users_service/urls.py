from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users_service.views import CreateUserView, LoginUserView, ManageUserView


urlpatterns = [
    path(
        "",
        CreateUserView.as_view(),
        name="register",
    ),
    path("me/", ManageUserView.as_view(), name="me"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]


app_name = "users_service"
