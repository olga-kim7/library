from django.urls import include, path
from rest_framework import routers

from books_service.views import BookViewSet

router = routers.DefaultRouter()
router.register("books", BookViewSet, basename="books")
urlpatterns = [
    path("", include(router.urls)),
]

app_name = "books_service"
