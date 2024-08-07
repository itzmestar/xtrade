from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django import forms
from .forms import APIKeyForm, BuyOrderForm, SellOrderForm, TradeHistoryForm
from .models import APIKey
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages
# Create your views here.
from .utils import Binance
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class KeyFormView(TemplateView):
    form_class = APIKeyForm
    template_name = 'keyform.html'
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            # try to fetch API keys
            instance = APIKey.objects.get(user=user)
            # create object of form
            form = self.form_class(request.POST, instance=instance)
            # check if form data is valid
            if form.is_valid():
                # save the form data to model
                form.save()
                messages.add_message(request, messages.SUCCESS,
                                     "Key saved Successfully.")

                return HttpResponseRedirect('/binance/home/')
        except APIKey.DoesNotExist:
            form = self.form_class(request.POST)
            # check if form data is valid
            if form.is_valid():
                apikey = form.save(commit=False)
                # commit=False tells Django that "Don't send this to database yet.
                apikey.user = request.user  # Set the user object here
                apikey.save()  # Now send it to DB
                messages.add_message(request, messages.SUCCESS,
                                     "Key saved Successfully.")
                return HttpResponseRedirect('/binance/home/')
        self.context['form'] = form
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'home.html'
    context = {}

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            # try to fetch API keys
            instance = APIKey.objects.get(user=user)
            api_key_saved = True
            binance = Binance(key=instance.api_key, secret=instance.api_secret)
            open_orders = binance.get_current_open_orders()
            '''open_orders = [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "orderListId": -1, # Unless OCO, the value will always be - 1
                "clientOrderId": "myOrder1",
                                 "price": "0.1",
            "origQty": "1.0",
            "executedQty": "0.0",
            "cummulativeQuoteQty": "0.0",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY",
            "stopPrice": "0.0",
            "icebergQty": "0.0",
            "time": 1499827319559,
            "updateTime": 1499827319559,
            "isWorking": True,
            "origQuoteOrderQty": "0.000000"
            },

                    {
                        "symbol": "BTCUSDT",
                        "orderId": 2,
                        "orderListId": -1, # Unless OCO, the value will always be - 1
                    "clientOrderId": "myOrder1",
                                     "price": "0.1",
            "origQty": "1.0",
            "executedQty": "0.0",
            "cummulativeQuoteQty": "0.0",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY",
            "stopPrice": "0.0",
            "icebergQty": "0.0",
            "time": 1499827319559,
            "updateTime": 1499827319559,
            "isWorking": True,
            "origQuoteOrderQty": "0.000000"
            }
            ]'''
            self.context['orders'] = open_orders
            self.context["listenKey"]= "btcusdt"
        except APIKey.DoesNotExist:
            api_key_saved = False
        self.context['api_key_saved'] = api_key_saved
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class BuyOrderView(TemplateView):
    form_class = BuyOrderForm
    template_name = 'buyform.html'
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            instance = APIKey.objects.get(user=user)
            # create object of form
            form = self.form_class(request.POST)
            # check if form data is valid
            if form.is_valid():
                #print(form.cleaned_data)
                param = {'symbol': None, 'type': None, 'price': None, 'quantity': None}
                for key in param.keys():
                    param[key] = form.cleaned_data[key]

                if request.POST.get('price'):
                    param['price'] = request.POST.get('price')

                binance = Binance(key=instance.api_key, secret=instance.api_secret)
                response = binance.place_buy_order(**param)
                if 'status' in response:
                    messages.add_message(request, messages.SUCCESS,
                                         f"Buy Order Submitted Successfully. Status:{response['status']}")
                elif 'msg' in response:
                    messages.add_message(request, messages.ERROR, f"Error in Order: {response['msg']}")
                else:
                    messages.add_message(request, messages.ERROR, "Buy Order Couldn't be submitted.")
                return HttpResponseRedirect('/binance/buy/')
        except APIKey.DoesNotExist:
            # if key doesn't exist redirect to key page
            messages.add_message(request, messages.WARNING, 'Please update Key-Secret.')
            return HttpResponseRedirect('/binance/keys/')

        self.context['form'] = form
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class SellOrderView(TemplateView):
    form_class = SellOrderForm
    template_name = 'sellform.html'
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            instance = APIKey.objects.get(user=user)
            # create object of form
            form = self.form_class(request.POST)
            # check if form data is valid
            if form.is_valid():
                # print(form.cleaned_data)
                param = {'symbol': None, 'type': None, 'price': None, 'quantity': None}
                for key in param.keys():
                    param[key] = form.cleaned_data[key]

                if request.POST.get('price'):
                    param['price'] = request.POST.get('price')

                binance = Binance(key=instance.api_key, secret=instance.api_secret)
                response = binance.place_sell_order(**param)
                if 'status' in response:
                    messages.add_message(request, messages.SUCCESS,
                                         f"Sell Order Submitted Successfully. Status:{response['status']}")
                elif 'msg' in response:
                    messages.add_message(request, messages.ERROR, f"Error in Order: {response['msg']}")
                else:
                    messages.add_message(request, messages.ERROR, "Sell Order Couldn't be submitted.")
                return HttpResponseRedirect('/binance/sell/')
        except APIKey.DoesNotExist:
            # if key doesn't exist redirect to key page
            messages.add_message(request, messages.WARNING, 'Please update Key-Secret.')
            return HttpResponseRedirect('/binance/keys/')

        self.context['form'] = form
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class CancelOrderView(View):

    def get(self, request):
        user = request.user
        try:
            instance = APIKey.objects.get(user=user)
            order_id = self.request.GET.get('order_id')
            symbol = self.request.GET.get('symbol')
            print(f'order_id={order_id} symbol={symbol}')
            if order_id is None or symbol is None:
                messages.add_message(request, messages.ERROR, "Can't Cancel. SYMBOL or Order ID missing.")
                return HttpResponseRedirect('/binance/home/')

            binance = Binance(key=instance.api_key, secret=instance.api_secret)
            response = binance.place_cancel_order(symbol=symbol, order_id=order_id)
            if 'status' in response:
                messages.add_message(request, messages.SUCCESS,
                                     f"Cancel Order Submitted Successfully. Status:{response['status']}")
            elif 'msg' in response:
                messages.add_message(request, messages.ERROR, f"Error in Cancel: {response['msg']}")
            else:
                messages.add_message(request, messages.ERROR, "Cancel Order Couldn't be submitted.")

        except APIKey.DoesNotExist:
            # if key doesn't exist redirect to key page
            messages.add_message(request, messages.WARNING, 'Please update Key-Secret.')
            return HttpResponseRedirect('/binance/keys/')

        # <view logic>
        return HttpResponseRedirect('/binance/home/')


@login_required
def keyform_view(request):
    context = {}

    if request.method == "POST":
        user = request.user
        try:
            instance = APIKey.objects.get(user=user)
            # create object of form
            form = APIKeyForm(request.POST, instance=instance)
            # check if form data is valid
            if form.is_valid():
                # save the form data to model
                form.save()
        except APIKey.DoesNotExist:
            form = APIKeyForm(request.POST)
            # check if form data is valid
            if form.is_valid():
                apikey = form.save(commit=False)
                # commit=False tells Django that "Don't send this to database yet.

                apikey.user = request.user  # Set the user object here
                apikey.save()  # Now send it to DB
    else:
        form = APIKeyForm()

    context['form'] = form
    return render(request, "keyform.html", context)


@method_decorator(login_required, name='dispatch')
class TradeHistoryView(TemplateView):
    form_class = TradeHistoryForm
    template_name = 'trade_history_form.html'
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            instance = APIKey.objects.get(user=user)
            # create object of form
            form = self.form_class(request.POST)
            # check if form data is valid
            if form.is_valid():

                binance = Binance(key=instance.api_key, secret=instance.api_secret)
                response = binance.fetch_trade_history(symbol=form.cleaned_data['symbol'])
                # convert timestamp to datetime string
                for r in response:
                    r['time'] = datetime.fromtimestamp(r['time']//1000).strftime('%Y-%m-%d %H:%M:%S')
                self.context['trade_history'] = response
                return render(request, 'trade_history.html', self.context)

                # return HttpResponseRedirect('/binance/trade-history/')
        except APIKey.DoesNotExist:
            # if key doesn't exist redirect to key page
            messages.add_message(request, messages.WARNING, 'Please update Key-Secret.')
            return HttpResponseRedirect('/binance/keys/')

        self.context['form'] = form
        return render(request, self.template_name, self.context)
