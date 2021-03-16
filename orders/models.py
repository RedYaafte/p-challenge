from django.utils import timezone
from django.db import models

from mongoengine import Document, fields


class Orders(Document):
    client = fields.StringField()
    products = fields.ListField(fields.DictField())
    total_price = fields.FloatField()
    user_email = fields.EmailField()

    created = fields.DateField(default=timezone.now)

    def __str__(self):
        return self.client


class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
