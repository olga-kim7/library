from datetime import date
from django.utils import timezone
import datetime

from unittest import TestCase

from django.contrib.auth import get_user_model

from books_service.models import Book
from borrowings_service.models import Borrowing, Payment
from users_service.models import User


def sample_book(**params):
    default = {
        "title": "Test Book",
        "author": "Test Author",
        "cover": "SOFT",
        "inventory": 10,
        "daily_fee": 10,
    }
    default.update(params)
    return Book.objects.create(**default)


def sample_user(**params):
    default = {
        "email": "mail@mail.com",
        "password": "PASSWORD",
    }
    default.update(params)
    return get_user_model().objects.create(**default)


def sample_borrowing(**params):
    default = {
        "borrowing_date": timezone.now(),
        "expected_date": timezone.now() + datetime.timedelta(days=1),
        "book_id": sample_book(**params),
        "user_id": sample_user(email="test@mail.com", password="PASSWORD"),
    }
    default.update(params)
    return Borrowing.objects.create(**default)


class TestBorrowingsModel(TestCase):
    def test_borrowings_str(self):
        user = User.objects.create(email="test_user@example.com")
        book = Book.objects.create(title="Test Book", author="Test Author", cover="Soft", inventory=10, daily_fee=5)

        borrowings = Borrowing.objects.create(
            borrowing_date=date(2022, 1, 1),
            expected_date=date(2022,10,10),
            actual_return=date(2022,10,11),
            book_id=book,
            user_id=user
        )
        expected_borrowings = f"{borrowings.borrowing_date} - {borrowings.actual_return}"
        self.assertEqual(str(borrowings), expected_borrowings)


class TestPaymentModel(TestCase):
    def test_payment_str(self):
        borrowing = sample_borrowing()

        payment = Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing_id=borrowing,
            session_url="http://example.com",
            session_id="test_session_id",
            money_to_pay=10
        )

        expected_borrowings = f"payment: {payment.status}, {payment.type}, {payment.borrowing_id}"
        self.assertEqual(str(payment), expected_borrowings)
