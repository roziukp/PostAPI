from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json
from .models import Post
from django.contrib.auth.models import User


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_post(title="", content=""):
        if title != "" and content != "":
            Post.objects.create(title=title, conntent=content)

    def login_a_user(self, username="", password=""):
        url = reverse(
            "login",
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing12233",
            first_name="test",
            last_name="user",
        )
        # add test data
        self.create_post("like glue", "sean pauldfsafdsafdsafdsafdsa")
        self.create_post("simple song", "konshensfdsafdsafdsa")
        self.create_post("love is wicke", "brick and lacfadsfadsfdsafsdafdsafdsae")


class AuthRegisterUserTest(APITestCase):

    def test_register_a_user_with_valid_data(self):
        url = reverse(
            "registration",
        )
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "username": "new_user",
                    "password": "new_passss123443",
                    "email": "new_user@mail.com"
                }
            ),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_a_user_with_invalid_data(self):
        url = reverse(
            "registration",
        )
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "username": "",
                    "password": "",
                    "email": ""
                }
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthLoginUserTest(BaseViewTest):

    def test_login_user_with_valid_credentials(self):
        response = self.login_a_user("test_user", "testing")
        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.login_a_user("anonymous", "pass")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
