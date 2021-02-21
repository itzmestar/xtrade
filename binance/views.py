from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from .forms import APIKeyForm
from .models import APIKey
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
# Create your views here.


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

        except APIKey.DoesNotExist:
            api_key_saved = False
            api_set_msg = ''
        self.context['api_key_saved'] = api_key_saved
        return render(request, self.template_name, self.context)


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


