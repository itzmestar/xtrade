from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django import forms
from .forms import APIKeyForm, BuyOrderForm, SellOrderForm
from .models import APIKey
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages
# Create your views here.
from .utils import Binance


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
                return HttpResponseRedirect('/binance/home/')
        except APIKey.DoesNotExist:
            form = self.form_class(request.POST)
            # check if form data is valid
            if form.is_valid():
                apikey = form.save(commit=False)
                # commit=False tells Django that "Don't send this to database yet.
                apikey.user = request.user  # Set the user object here
                apikey.save()  # Now send it to DB
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

            if request.session.get('binance'):
                #binance = request.session['binance']
                pass
            else:
                #binance = Binance(instance.api_key, instance.api_secret)
                #request.session['binance'] = binance
                pass

            #open_orders = binance.get_current_open_orders()
            open_orders = [
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
            }

            ]
            self.context['orders'] = open_orders
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
                    messages.add_message(request, messages.SUCCESS, 'Buy Order Submitted Successfully.')
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
            # create object of form
            form = self.form_class(request.POST)
            # check if form data is valid
            if form.is_valid():
                return HttpResponseRedirect('/binance/home/')
        except APIKey.DoesNotExist:
            pass
        self.context['form'] = form
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class CancelOrderView(TemplateView):
    pass


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

