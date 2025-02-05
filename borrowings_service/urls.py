from django.urls import include, path
from rest_framework import routers

from borrowings_service import views
from borrowings_service.views import BorrowingsViewSet, PaymentViewSet, SuccessView, CancelView, my_webhook_view

router = routers.DefaultRouter()
router.register("borrowings", BorrowingsViewSet)
router.register("payment", PaymentViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("webhook/", my_webhook_view, name="webhook"),
]


app_name = "borrowings_service"
