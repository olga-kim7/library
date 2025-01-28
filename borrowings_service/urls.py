from django.urls import include, path
from rest_framework import routers

from books_service.views import BookViewSet
from borrowings_service.views import BorrowingsViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingsViewSet)
urlpatterns = [
    path("", include(router.urls)),
]

app_name = "borrowings_service"
