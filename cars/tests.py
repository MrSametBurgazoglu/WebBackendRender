from django.test import TestCase

from cars.models import Car, Location
from cars.utils import create_customer, create_token, create_test_cars


class CustomerTest(TestCase):

    def test_get_car_nearby(self):
        create_test_cars()
        user = create_customer().user
        token = create_token(user)
        response = self.client.get("/api/cars/", {
            "latitude": "1",
            "longtitude": "1",

        },
                                    content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 200)

    def test_get_car_detail(self):
        create_test_cars()
        first_car = Car.objects.first()
        user = create_customer().user
        token = create_token(user)
        response = self.client.get("/api/cars/{id}/".format(id=first_car.id),
                                   content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 200)

    def test_delete_car_detail(self):
        create_test_cars()
        first_car = Car.objects.first()
        user = create_customer().user
        token = create_token(user)
        response = self.client.delete("/api/cars/{id}/".format(id=first_car.id),
                                   content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 204)

    def test_change_car_active(self):
        create_test_cars()
        first_car = Car.objects.first()
        user = create_customer().user
        token = create_token(user)
        response = self.client.post("/api/cars/{id}/change_state/".format(id=first_car.id),
                                   content_type="application/json",
                                   **{'HTTP_AUTHORIZATION': f'Token {token.key}'})
        self.assertEqual(response.status_code, 200)
