from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from accounts.models import Customer
from rest_framework.authtoken.models import Token


class CustomerTest(TestCase):

    def create_customer(self):
        user = User.objects.create(
            username="MrSametBurgazoğlu",
            email="sametburgazoglu@gmail.com",
            first_name="Samet",
            last_name="Burgazoğlu"
        )
        user.set_password("54M3754m37")
        user.save()
        customer = Customer.objects.create(
            phone_number="123213123",
            full_name=" ".join([user.first_name, user.last_name]),
            email=user.email,
            user=user,
        )
        customer.save()
        return customer

    def create_token(self, user):
        token = Token.objects.create(user=user)
        return token

    def test_create_user(self):
        response = self.client.post("/api/accounts/customers/", {
            "phone_number": "123213123",
            "user": {
                "username": "MrSametBurgazoğlu",
                "email": "sametburgazoglu@gmail.com",
                "password": "54M3754m37",
                "first_name": "Samet",
                "last_name": "Burgazoğlu",
            },
        },
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_get_token(self):
        self.create_customer()
        response = self.client.post("/api/accounts/api-token-auth/", {
            "username": "MrSametBurgazoğlu",
            "password": "54M3754m37",
        },
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_customer(self):
        user = self.create_customer().user
        token = self.create_token(user)
        response = self.client.put("/api/accounts/customers/{user_id}/".format(user_id=user.id), {
            "phone_number": "1232131233",
            "user": {
                "username": "MrSametBurgazoğlu2",
                "email": "sametburgazoglu@gmail2.com",
                "password": "54M3754m372",
                "first_name": "Samet2",
                "last_name": "Burgazoğlu2",
            },
        },
                                    content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 200)

    def test_delete_customer(self):
        user = self.create_customer().user
        token = self.create_token(user)
        response = self.client.delete("/api/accounts/customers/{user_id}/".format(user_id=user.id),
                                      content_type="application/json",
                                      **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 204)



# Create your tests here.
