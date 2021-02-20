from django.shortcuts import render
from .forms import APIKeyForm
from .models import APIKey
from django.contrib.auth.decorators import login_required
# Create your views here.


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
