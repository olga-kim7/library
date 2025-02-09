from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from books_service.models import Book
from books_service.serializers import BookSerializer

BOOK_URL = reverse("books_service:books-list")


def detail_url(book_id):
    return reverse("books_service:books-detail", kwargs={"pk": book_id})


def sample_book(**params) -> Book:
    defaults = {
        "title": "Test Book",
        "author": "Test Author",
        "cover": "SOFT",
        "inventory": 12,
        "daily_fee": 10,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_not_auth_required(self):
        response = self.client.get(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_auth_required_for_detail(self):
        book = sample_book()
        response = self.client.get(detail_url(book.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = sample_book()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="Test123456",
        )
        self.client.force_authenticate(self.user)

    def test_auth_required(self):
        response = self.client.get(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_book_for_detail(self):
        book = sample_book()
        response = self.client.get(detail_url(book.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_books_list(self):
        sample_book()

        response = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], serializer.data[0])

    def test_create_book(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 11,
            "daily_fee": 14,
        }
        response = self.client.post(BOOK_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_book(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 11,
            "daily_fee": 16,
        }
        url = detail_url(self.book.pk)
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book(self):
        url = detail_url(self.book.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = sample_book()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="Test12345",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_book_admin(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 11,
            "daily_fee": 16,
        }
        response = self.client.post(BOOK_URL, payload)
        book = Book.objects.get(pk=response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(book, key))

    def test_put_book_admin(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "SOFT",
            "inventory": 11,
            "daily_fee": 16,
        }
        url = detail_url(self.book.pk)
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book_admin(self):
        url = detail_url(self.book.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
