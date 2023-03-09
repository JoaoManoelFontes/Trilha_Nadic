from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Book, Category


class UrlTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

        self.book = Book.objects.create(
            category=self.category,
            synopsis="Test Synopsis",
            title="Test Book",
            author_name="Test Author",
            publishing_company_name="Test Publishing Company",
            release_year="2020-01-01",
            price=10.0,
            quantity=10,
        )

    def test_home_url(self):
        url = reverse("home")
        self.assertEqual(resolve(url).view_name, "home")

    def test_sale_url(self):
        url = reverse("sale", args=[self.book.id])
        self.assertEqual(resolve(url).view_name, "sale")

    def test_register_book_url(self):
        url = reverse("register_book")
        self.assertEqual(resolve(url).view_name, "register_book")

    def test_update_book_url(self):
        url = reverse("update_book", args=[self.book.id])
        self.assertEqual(resolve(url).view_name, "update_book")

    def test_delete_book_url(self):
        url = reverse("delete_book", args=[self.book.id])
        self.assertEqual(resolve(url).view_name, "delete_book")

    def test_add_book_url(self):
        url = reverse("add_book", args=[self.book.id])
        self.assertEqual(resolve(url).view_name, "add_book")

    def test_register_category_url(self):
        url = reverse("register_category")
        self.assertEqual(resolve(url).view_name, "register_category")

    def test_sales_history_url(self):
        url = reverse("sales_history")
        self.assertEqual(resolve(url).view_name, "sales_history")
