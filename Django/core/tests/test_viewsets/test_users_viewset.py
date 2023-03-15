from ..setup import MainTest
from django.contrib.auth.models import User


class TestUserViewSet(MainTest):
    def test_authentication(self):
        response = self.api_client.get("/api/users/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided."
        )

    def test_users_list(self):
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.api_client.get(self.users_api_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["username"], str(self.user.username))
        self.assertFalse(response.json()[0]["is_superuser"])

        self.api_client.logout()

    def test_create_user_without_authentication(self):
        response = self.api_client.post(
            self.users_api_url,
            data={"username": "test_user2", "password": "test_password2", "email": ""},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "test_user2")
        self.assertFalse(response.json()["is_superuser"])

    def test_update_user(self):
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.api_client.patch(
            self.users_api_url + f"{self.user.id}/",
            data={"email": "test@testmail.com"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=self.user.id).email, "test@testmail.com")

        self.api_client.logout()

    def test_delete_user(self):
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.api_client.delete(self.users_api_url + f"{self.user.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

        self.api_client.logout()
