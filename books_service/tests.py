from django.test import TestCase

from books_service.models import Book


class BooksServiceTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Test Cover",
            inventory=13,
            daily_fee=10
        )
        self.book2 = Book.objects.create(
            title="Test Book2",
            author="Test Author2",
            cover="Test Cover2",
            inventory=13,
            daily_fee=10
        )
