from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class AuthTestCase(TestCase):
    def setUp(self):
        self.payload = {
            "username": "omniman",
            "password": "123456",
        }
        User.objects.create_superuser(
            self.payload["username"], f"{self.payload['username']}@mail.com", self.payload["password"]
        )
        self.client = Client()

    def test_auth_obtain_token(self):
        response = self.client.post(reverse("token_obtain_pair"), data=self.payload)
        assert response.status_code == 200
        assert response.json()["access"] is not None

    def test_auth_refresh_token(self):
        response = self.client.post(reverse("token_obtain_pair"), data=self.payload)
        refresh = response.json()["refresh"]
        response = self.client.post(reverse("token_refresh"), data={"refresh": refresh})
        assert response.status_code == 200
        assert response.json()["access"] is not None
