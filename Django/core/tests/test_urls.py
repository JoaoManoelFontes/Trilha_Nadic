from django.urls import resolve

from .setup import MainTest

# from django.contrib.auth.models import User


class UrlTest(MainTest):
    def test_home_url(self):
        self.assertEqual(resolve(self.home_url).view_name, "home")

    def test_sale_url(self):
        self.assertEqual(resolve(self.sale_url).view_name, "sale")

    def test_register_book_url(self):
        self.assertEqual(
            resolve(self.register_book_url).view_name, "register_book"
        )  # noqa

    def test_update_book_url(self):
        self.assertEqual(resolve(self.update_book_url).view_name, "update_book")  # noqa

    def test_delete_book_url(self):
        self.assertEqual(resolve(self.delete_book_url).view_name, "delete_book")  # noqa

    def test_add_book_url(self):
        self.assertEqual(resolve(self.add_book_url).view_name, "add_book")

    def test_register_category_url(self):
        self.assertEqual(
            resolve(self.register_category_url).view_name, "register_category"
        )  # noqa

    def test_sales_history_url(self):
        self.assertEqual(
            resolve(self.sales_history_url).view_name, "sales_history"
        )  # noqa
