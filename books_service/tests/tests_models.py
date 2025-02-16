from django.test import TestCase

from books_service.models import Book


class BooksServiceTestCase(TestCase):
    def test_book_str(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Soft",
            inventory=12,
            daily_fee=10,
        )
        expected = f"{book.title} - {book.author}"
        self.assertEqual(str(book), expected)
