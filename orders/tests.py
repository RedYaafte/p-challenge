import datetime
from itertools import islice

from django.test import TestCase
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from .models import Orders, Product


class TestProductViewSet(TestCase):
    def setUp(self):
        self.url = '/api/product/'
        self.client = APIClient()
        self.data = {
            'name': 'tamal',
            'price': 12
        }

    def create_product(self):
        return Product.objects.create(
            name='chilaquiles',
            price=30
        )

    def test_product_list_200(self):
        self.create_product()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create_201(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_retrive_200(self):
        p = self.create_product()
        response = self.client.get(f'{self.url}{p.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], p.id)

    def test_product_update_200(self):
        p = self.create_product()
        data = {'price': 45}
        response = self.client.patch(f'{self.url}{p.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['price'], data['price'])

    def test_product_destroy_204(self):
        p = self.create_product()
        response = self.client.delete(f'{self.url}{p.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestOrderViewSet(TestCase):
    def setUp(self):
        self.url = '/api/order/'
        self.client = APIClient()

    def test_create_order_201(self):
        data = {
            'client': 'Paco',
            'products': [
                {
                    'name': 'taco',
                    'price': 10,
                    'qty': 10
                }
            ],
            'total_price': 100
        }
        r = self.client.post(self.url, data, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        # Delete Order from database
        o = Orders.objects.filter(id=r.json()['id']).delete()
        self.assertTrue(o)

    def test_method_get_not_allowed(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestReportViewSet(TestCase):
    def setUp(self):
        self.url = '/api/report/'
        self.client = APIClient()
        self.products = [
            {
                'name': 'taco',
                'price': 10,
                'qty': 10
            },
            {
                'name': 'quesadilla',
                'price': 15,
                'qty': 5
            },
            {
                'name': 'torta de jamon',
                'price': 25,
                'qty': 5
            }
        ]

    def create_order(self):
        batch_size = 100
        objs = (Orders(client='test-orders-mongo', products=self.products,
                       total_price=300, user_email='test@test.com')
                for i in range(1000))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Orders.objects.insert(batch, batch_size)

        for p in self.products:
            Product.objects.create(name=p['name'], price=p['price'])

    def test_get_report_list(self):
        date = timezone.now()
        self.create_order()

        r = self.client.get(
            f'{self.url}?start-date={date.date()}&end-date={date.date()}',
            forma='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        # Delete Orders from database
        d = Orders.objects.filter(
            client='test-orders-mongo', products=self.products).delete()
        self.assertEqual(d, 1000)
