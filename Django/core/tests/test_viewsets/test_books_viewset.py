from ...models import Book, Category
from ..setup import MainTest


class TestViewSets(MainTest):
    def test_authentication(self):
        response = self.api_client.get("/api/books/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_books_list(self):
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.api_client.get(self.books_api_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], str(self.book.id))

        self.api_client.logout()

    def test_book_retrieve(self):
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.api_client.get(self.books_api_url + str(self.book.id) + "/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], str(self.book.id))

        self.api_client.logout()

    def test_book_create(self):
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.api_client.post(
            self.books_api_url,
            {
                "category": {"name": "Test Category 2"},
                "synopsis": "Test Synopsis 2",
                "title": "Test Book 2",
                "author_name": "Test Author 2",
                "publishing_company_name": "Test Publishing Company 2",
                "release_year": "2020-02-02",
                "price": 11.0,
                "quantity": 11,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Book.objects.filter(title=response.json()["title"]).exists())
        self.assertTrue(
            Category.objects.filter(name=response.json()["category"]["name"]).exists()
        )

        self.api_client.logout()

    def test_book_update(self):
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.api_client.patch(
            self.books_api_url + str(self.book.id) + "/",
            {
                "category": {"name": "Test Category 3"},
                "title": "Updated Title",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Title")
        self.assertTrue(response.json()["category"]["name"] != self.category.name)

        self.api_client.logout()

    def test_book_delete(self):
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.api_client.delete(self.books_api_url + str(self.book.id) + "/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

        self.api_client.logout()
