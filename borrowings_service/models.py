import uuid
from datetime import date

import stripe
from django.conf import settings
from django.db import models
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError

from books_service.models import Book


class Borrowing(models.Model):
    borrowing_date = models.DateField(auto_now=False, auto_now_add=False)
    expected_date = models.DateField(auto_now=False, auto_now_add=False)
    actual_return = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrowings')

    @property
    def total_price(self):
        end_date = self.actual_return if self.actual_return else self.expected_date
        days_borrowed = (end_date - self.borrowing_date).days
        return days_borrowed * self.book_id.daily_fee if days_borrowed > 0 else 0

    def __str__(self):
        return f"{self.borrowing_date} - {self.actual_return}"

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
        ('PENDING', 'PENDING'),
        ('PAID', 'PAID')
    ]
    TYPE = [
        ('PAYMENT', 'PAYMENT'),
        ('FINE', 'FINE')
    ]

    status = models.CharField(max_length=255, choices=STATUS, default='PEC')
    type = models.CharField(max_length=255, choices=TYPE, default='PC')
    borrowing_id = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name='payments')
    session_url = models.URLField(blank=True, null=True)
    session_id = models.CharField(blank=True, null=True, max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
