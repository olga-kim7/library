from rest_framework import serializers

from books_service.serializers import BookSerializer
from borrowings_service.models import Borrowing, Payment
from users_service.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingListSerializer(BorrowingSerializer):
    # book_id = BookSerializer(read_only=True)
    # user_id = UserSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = "__all__"

    def get_total_price(self, obj):
        return obj.total_price


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
