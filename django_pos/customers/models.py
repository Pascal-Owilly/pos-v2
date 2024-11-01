from django.db import models
from django.forms import model_to_dict
import django.utils.timezone


class Customer(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    address = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    date_added = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        db_table = 'Customers'

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def to_select2(self):
        item = {
            "label": self.get_full_name(),
            "value": self.id
        }
        return item

class Supplier(models.Model):
    name = models.CharField(max_length=256)
    address = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    date_added = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        db_table = 'Suppliers'

    def __str__(self) -> str:
        return self.name

    def to_select2(self):
        item = {
            "label": self.name(),
            "value": self.id
        }
        return item