from django.shortcuts import render
from rest_framework import viewsets

from borrowings_service.models import Borrowing
from borrowings_service.serializers import BorrowingSerializer, BorrowingListSerializer


class BorrowingsViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return BorrowingListSerializer
        return BorrowingSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            return queryset.select_related()
        return queryset
