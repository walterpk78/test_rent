from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .constants import TRANSPORT_TYPE, MAX_CASH_AMOUNT
from django.db.models import Sum, Count, Max, Q


class TransportManager(models.Manager):
    def list(self, agency_id, filters=None, order_by=None, from_row=0, to_row=10):
        pass


class Transport(models.Model):
    transport_type      = models.IntegerField(choices=TRANSPORT_TYPE, db_index=True, null=True)
    description         = models.TextField(null=True)
    price_per_day       = models.BigIntegerField(default=0)
    km                  = models.BigIntegerField(default=0, null=True)

    objects = TransportManager()

    class Meta:
        app_label = 'rentomatic'


class Rent(models.Model):
    transport          = models.ForeignKey(Transport, related_name='transport')
    start_date         = models.DateField(db_index=True, null=True)
    end_date           = models.DateField(db_index=True, null=True)
    first_name         = models.CharField(max_length=50)
    last_name          = models.CharField(max_length=50, null=True, blank=True)
    email              = models.CharField(max_length=254, null=True, blank=True)
    phone              = models.CharField(max_length=20, null=True, blank=True)
    creation_time      = models.DateTimeField(auto_now_add=True)
    amount             = models.BigIntegerField(validators=[MinValueValidator(0), MaxValueValidator(MAX_CASH_AMOUNT)])
    rented             = models.BooleanField(default=False)
    class Meta:
        app_label = 'rentomatic'
