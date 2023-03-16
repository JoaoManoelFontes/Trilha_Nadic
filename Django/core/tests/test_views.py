from .setup import MainTest
from ..models import Book, Category, Sale


class ViewTest(MainTest):
    def test_home_without_user(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)

    def test_home_with_user(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

        self.client.logout()

    def test_sale_get(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(self.sale_url)

        self.assertTemplateUsed(response, "sale.html")
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_sale_post(self):
        self.client.login(username=self.user.username, password=self.user_password)

        response = self.client.post(
            self.sale_url,
            {
                "client": "test client",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Book.objects.get(pk=self.book.id).quantity, self.book.quantity - 1
        )
        self.assertEqual(Sale.objects.count(), 1)
        self.assertEqual(Sale.objects.get(book=self.book).client_name, "test client")

        self.client.logout()

    def test_add_book(self):
        response = self.client.get(self.add_book_url, {"quantity": 10})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Book.objects.get(pk=self.book.id).quantity, self.book.quantity + 10
        )

        self.client.logout()

    def test_register_book_get(self):
        response = self.client.get(self.register_book_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book_form.html")

    def test_register_book_post(self):
        response = self.client.post(
            self.register_book_url,
            {
                "category": self.category.id,
                "synopsis": "Test Synopsis 2",
                "title": "Test Book 2",
                "author_name": "Test Author 2",
                "publishing_company_name": "Test Publishing Company 2",
                "release_year": "2022-02-02",
                "price": 11.0,
                "quantity": 11,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 2)
        self.assertTrue(Book.objects.filter(title="Test Book 2").exists())

    def test_register_category_get(self):
        response = self.client.get(self.register_category_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "category_form.html")

    def test_register_category_post(self):
        response = self.client.post(
            self.register_category_url, {"name": "Test Category 2"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 2)
        self.assertTrue(Category.objects.filter(name="Test Category 2").exists())

    def test_update_book_get(self):
        response = self.client.get(self.update_book_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "book_form.html")

    def test_update_book_post(self):
        response = self.client.post(
            self.update_book_url,
            {
                "category": self.category.id,
                "synopsis": "Test Synopsis",
                "title": "Updated Title",
                "author_name": "Test Author",
                "publishing_company_name": "Test Publishing Company",
                "release_year": "2020-01-01",
                "price": 10.0,
                "quantity": 10,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get(pk=self.book.id).title, "Updated Title")

    def test_delete_book(self):
        response = self.client.get(self.delete_book_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 0)

    def test_sales_history(self):
        response = self.client.get(self.sales_history_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales.html")

    def test_user_sales_history(self):
        self.client.login(username=self.user.username, password=self.user_password)

        response = self.client.get(self.sales_history_url, {"seller": self.user_name})

        self.assertEqual(response.status_code, 200)

        self.client.logout()
