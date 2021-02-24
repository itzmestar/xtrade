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


class Order(models.Model):
    """
    Store Buy/Sell Orders
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )
    symbol = models.CharField(verbose_name="SYMBOL", max_length=100,)
    orderId = models.CharField(verbose_name="ORDERID", max_length=100,)
    orderListId = models.CharField(verbose_name="ORDERLISTID", max_length=100,)
    clientOrderId = models.CharField(verbose_name="CLIENTORDERID", max_length=100,)
    price = models.CharField(verbose_name="PRICE", max_length=100,)
    origQty = models.CharField(verbose_name="ORIGQTY", max_length=100,)
    executedQty = models.CharField(verbose_name="EXECUTEDQTY", max_length=100,)
    cummulativeQuoteQty = models.CharField(verbose_name="CUMMULATIVEQUOTEQTY", max_length=100,)
    status = models.CharField(verbose_name="STATUS", max_length=100,)
    timeInForce = models.CharField(verbose_name="TIMEINFORCE", max_length=100,)
    type = models.CharField(verbose_name="TYPE", max_length=100,)
    side = models.CharField(verbose_name="SIDE", max_length=100,)
    stopPrice = models.CharField(verbose_name="STOPPRICE", max_length=100,)
    icebergQty = models.CharField(verbose_name="ICEBERGQTY", max_length=100,)
    time = models.CharField(verbose_name="TIME", max_length=100,)
    updateTime = models.CharField(verbose_name="UPDATETIME", max_length=100,)
    isWorking = models.CharField(verbose_name="ISWORKING", max_length=100,)
    origQuoteOrderQty = models.CharField(verbose_name="ORIGQUOTEORDERQTY", max_length=100,)
