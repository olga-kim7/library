from rest_framework import serializers

from borrowings_service.models import Borrowing, Payment


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingListSerializer(BorrowingSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = "__all__"

    def get_total_price(self, obj):
        return obj.total_price


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
