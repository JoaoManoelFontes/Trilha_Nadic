from django.test import TestCase, Client

from django.urls import reverse

from django.contrib.auth.models import User

from ..models import Book, Category


class MainTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_password = "test"
        self.user_name = "testuser"

        self.user = User.objects.create(
            username="testuser",
        )
        self.user.set_password(self.user_password)
        self.user.save()

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

        self.home_url = reverse("home")
        self.sale_url = reverse("sale", args=[self.book.id])
        self.add_book_url = reverse("add_book", args=[self.book.id])
        self.register_book_url = reverse("register_book")
        self.register_category_url = reverse("register_category")
        self.update_book_url = reverse("update_book", args=[self.book.id])
        self.delete_book_url = reverse("delete_book", args=[self.book.id])
        self.sales_history_url = reverse("sales_history")
