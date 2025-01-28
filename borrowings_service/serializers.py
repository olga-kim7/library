from rest_framework import serializers

from books_service.serializers import BookSerializer
from borrowings_service.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrowing_data", "expected_date", 'actual_return', 'book_id', 'user_id')


class BorrowingListSerializer(BorrowingSerializer):
    book_id = BookSerializer()
