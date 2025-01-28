import uuid

from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError

from books_service.models import Book


class Borrowing(models.Model):
    borrowing_data = models.DateField(auto_now=False, auto_now_add=False)
    expected_date = models.DateField(auto_now=False, auto_now_add=False)
    actual_return = models.DateField(auto_now=False, auto_now_add=False)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrowings')

    def __str__(self):
        return f"{self.borrowing_data} - {self.actual_return}"

    def valid_data(self):
        if self.book_id.inventory == 0:
            raise ValidationError("This book is not borrowing")

    def clean(self):
        super().clean()
        self.valid_data()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)




class Payment(models.Model):
    STATUS = [
        ('PEC', 'PENDING'),
        ('PAC', 'PAID')
    ]
    TYPE = [
        ('PC', 'PAYMENT'),
        ('FC', 'FINE')
    ]

    status = models.CharField(max_length=255, choices=STATUS)
    type = models.CharField(max_length=255, choices=TYPE)
    borrowing_id = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name='payments')
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)

