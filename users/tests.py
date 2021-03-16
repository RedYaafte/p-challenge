from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status


class TestUser(TestCase):
    def setUp(self):
        self.url = '/api/user/'
        self.client = APIClient()

    def test_create_user_201(self):
        data = {
            'email': 'test@test.com',
            'name': 'Test'
        }
        r = self.client.post(self.url, data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_method_get_not_allowed(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
