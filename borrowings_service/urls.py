from django.urls import include, path
from rest_framework import routers

from borrowings_service.views import (
    BorrowingsViewSet,
    PaymentViewSet,
    CancelView,
    my_webhook_view,
)

router = routers.DefaultRouter()
router.register("borrowings", BorrowingsViewSet, basename="borrowings")
router.register("payment", PaymentViewSet, basename="payments")
urlpatterns = [
    path("", include(router.urls)),
    # path("success/", SuccessView.as_view(), name="success"),
    # path("cancel/", CancelView.as_view(), name="cancel"),
]


app_name = "borrowings_service"
