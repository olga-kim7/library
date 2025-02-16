from django.urls import include, path
from rest_framework import routers

from borrowings_service.views import (
    BorrowingsViewSet,
    PaymentViewSet,
)

router = routers.DefaultRouter()
router.register("borrowings", BorrowingsViewSet, basename="borrowings")
router.register("payment", PaymentViewSet, basename="payments")
urlpatterns = [
    path("", include(router.urls)),
]


app_name = "borrowings_service"
