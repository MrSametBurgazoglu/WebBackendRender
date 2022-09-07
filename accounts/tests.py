from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from accounts.models import Customer
from rest_framework.authtoken.models import Token
from cars.utils import create_customer, create_token


class CustomerTest(TestCase):
    def test_create_user(self):
        response = self.client.post("/api/accounts/customers/", {
            "name": "SametBurgazoğlu",
            "phone": "123213123",
            "email": "sametburgazoglu@gmail.com",
            "password": "54M3754m37",
        },
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_get_token(self):
        create_customer()
        response = self.client.post("/api/accounts/api-token-auth/", {
            "email": "sametburgazoglu@gmail.com",
            "password": "54M3754m37",
        },
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_customer(self):
        user = create_customer().user
        token = create_token(user)
        response = self.client.put("/api/accounts/customers/{user_id}/".format(user_id=user.id), {
            "name": "SametBurgazoğlu2",
            "phone": "1232131232",
            "email": "sametburgazoglu@gmail.com",
            "password": "54M3754m37",
        },
                                    content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 200)

    def test_delete_customer(self):
        user = create_customer().user
        token = create_token(user)
        response = self.client.delete("/api/accounts/customers/{user_id}/".format(user_id=user.id),
                                      content_type="application/json",
                                      **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 204)



# Create your tests here.
