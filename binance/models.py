from django.db import models
from django.contrib.auth.models import User

from django.db.models.fields import CharField
from binance.cipher import decrypt, encrypt


class EnField(CharField):
    def from_db_value(self, value, expression, connection):
        """ Decrypt the data for display in Django as normal. """
        return decrypt(value)

    def get_prep_value(self, value):
        """ Encrypt the data when saving it into the database. """
        return encrypt(value)

# Create your models here.


class APIKey(models.Model):
    """
    Store API Key & Secret using encryption
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False
    )

    api_key = EnField(
        verbose_name="API Key",
        max_length=100,
        null=False,
        editable=True
    )

    api_secret = EnField(
        verbose_name="API Secret",
        max_length=100,
        null=False,
        editable=True
    )
