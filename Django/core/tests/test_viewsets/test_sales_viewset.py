from ...models import Sale
from django.contrib.auth.models import User
from ..setup import MainTest


class TestSalesViewsets(MainTest):
    def test_authentication(self):
        response = self.api_client.get(self.sales_api_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_sales_list(self):
        Sale.objects.create(
            book=self.book,
            seller=self.user,
            client_name="Test Client",
        )

        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.api_client.get(self.sales_api_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["book"]["title"], self.book.title)
        self.assertEqual(response.json()[0]["seller"]["username"], self.user.username)

        self.api_client.logout()

    def test_billing_authentication(self):
        # Somente superusers podem acessar a rota de billing
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.api_client.get(self.sales_api_url + "billing/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )

        self.api_client.logout()

    def test_billing_superuser(self):
        self.superuser = User.objects.create(
            username=self.superuser_name,
            is_superuser=True,
            is_staff=True,
        )
        self.superuser.set_password(self.superuser_password)
        self.superuser.save()

        token = self.api_client.post(
            self.token_url,
            {
                "username": self.superuser_name,
                "password": self.superuser_password,
            },
        ).json()["access"]

        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.api_client.get(self.sales_api_url + "billing/")

        billing = Sale.objects.all().values_list("book__price", flat=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()["faturamento"], sum(billing))

        self.api_client.logout()
