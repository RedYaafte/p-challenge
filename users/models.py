from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=250)
    name = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
