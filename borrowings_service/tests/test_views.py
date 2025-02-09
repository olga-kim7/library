from django.utils import timezone
import datetime


from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books_service.models import Book
from borrowings_service.models import Borrowing, Payment
from borrowings_service.serializers import BorrowingSerializer
from users_service.models import User

BORROWING_URL = reverse("borrowings_service:borrowings-list")
PAYMENT_LIST = reverse("borrowings_service:payments-list")


def detail_url(borrowing_id):
    return reverse("borrowings_service:borrowings-detail", args=[borrowing_id])


def payment_url(payment_id):
    return reverse("borrowings_service:payments-detail", args=[payment_id])


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


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_detail(self):
        borrowing = sample_borrowing()
        response = self.client.get(detail_url(borrowing.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_payment_details(self):
        url = payment_url(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_payment_list(self):
        response = self.client.get(PAYMENT_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.borrowing = sample_borrowing()
        self.book = sample_book()
        self.user = get_user_model().objects.create_user(
            email="admiesfdsdfsdfsn@ad.com",
            password="<PASSWORD>",
            is_staff=False,
        )
        self.book = sample_book()

        self.client.force_authenticate(self.user)

    def test_auth_required(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_required_for_detail(self):
        response = self.client.get(detail_url(self.borrowing.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_borrowing_list(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payments_money_to_pay_property(self):
        payment = Payment.objects.create(
            status="Pending",
            type="Payment",
            borrowing_id=self.borrowing,
        )
        self.borrowing.actual_return = (
            timezone.now() + datetime.timedelta(days=1)
        )
        self.borrowing.save()
        expected_charge = payment.money_to_pay
        self.assertEqual(payment.money_to_pay, expected_charge)

    def test_post_method_borrowings(self):
        book = sample_book(
            title="Test Booking.com",
        )
        data = {
            "borrowing_date": timezone.now().date(),
            "expected_date": timezone.now().date(),
            "book_id": book.id,
            "user_id": self.user.id,
        }
        response = self.client.post(BORROWING_URL, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_method_borrowings(self):
        url = detail_url(self.borrowing.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
