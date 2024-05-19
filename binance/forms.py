# import form class from django
from django import forms
# import GeeksModel from models.py
from .models import APIKey
from .utils import Binance

SYMBOLS = Binance.get_trading_symbols()


# create a buy order form
class BuyOrderForm(forms.Form):
    BUY_TYPE = [('MARKET', 'MARKET'), ('LIMIT', 'LIMIT')]

    symbol = forms.CharField(label='Symbol', required=True, widget=forms.Select(choices=SYMBOLS))
    type = forms.CharField(label='Buy Type', required=True, widget=forms.Select(choices=BUY_TYPE))
    price = forms.FloatField(label='Price', required=False, disabled=True)
    quantity = forms.FloatField(label='Quantity', required=True)


# create a sell order form
class SellOrderForm(forms.Form):
    SELL_TYPE = [('MARKET', 'MARKET'), ('LIMIT', 'LIMIT'), ]
    #SYMBOLS = Binance.get_trading_symbols()
    symbol = forms.CharField(label='Symbol', required=True, widget=forms.Select(choices=SYMBOLS))
    type = forms.CharField(label='Sell Type', required=True, widget=forms.Select(choices=SELL_TYPE))
    price = forms.FloatField(label='Price', required=False, disabled=True)
    quantity = forms.FloatField(label='Quantity', required=True)


# create a ModelForm
class APIKeyForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = APIKey
        fields = ['api_key', 'api_secret']


class TradeHistoryForm(forms.Form):

    symbol = forms.CharField(label='Symbol', required=True, widget=forms.Select(choices=SYMBOLS))


