from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.models import Customer
from cars.models import Car, Location
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

    def create_test_cars(self):
        location1 = Location.objects.create(latitude=1.0, longitude=1.0)
        location2 = Location.objects.create(latitude=111.0, longitude=1.0)
        location3 = Location.objects.create(latitude=1.0, longitude=111.0)
        location4 = Location.objects.create(latitude=1.0, longitude=1.0)
        location5 = Location.objects.create(latitude=1.0, longitude=1.0)
        location1.save()
        location2.save()
        location3.save()
        location4.save()
        location5.save()
        Car.objects.bulk_create([
            Car(brand="brand", model="model", segment="segment", licence="ABC 123 ABC", location=location1),
            Car(brand="brand", model="model", segment="segment", licence="ABC 124 ABC", location=location2),
            Car(brand="brand", model="model", segment="segment", licence="ABC 125 ABC", location=location3),
            Car(brand="brand", model="model", segment="segment", licence="ABC 126 ABC", location=location4),
            Car(brand="brand", model="model", segment="segment", licence="ABC 127 ABC", location=location5),
        ])

    def test_get_car_nearby(self):
        self.create_test_cars()
        user = self.create_customer().user
        token = self.create_token(user)
        response = self.client.get("/api/cars/", {
            "latitude": "1",
            "longtitude": "1",

        },
                                    content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 200)

    def test_get_car_detail(self):
        self.create_test_cars()
        first_car = Car.objects.first()
        user = self.create_customer().user
        token = self.create_token(user)
        response = self.client.get("/api/cars/{id}/".format(id=first_car.id),
                                   content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 200)

    def test_delete_car_detail(self):
        self.create_test_cars()
        first_car = Car.objects.first()
        user = self.create_customer().user
        token = self.create_token(user)
        response = self.client.delete("/api/cars/{id}/".format(id=first_car.id),
                                   content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 204)

    def test_change_car_active(self):
        self.create_test_cars()
        first_car = Car.objects.first()
        user = self.create_customer().user
        token = self.create_token(user)
        response = self.client.post("/api/cars/{id}/change_state/".format(id=first_car.id),
                                   content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 200)
