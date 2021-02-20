from django.contrib import admin

# Register your models here.
from .models import APIKey


class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_key', 'api_secret')


admin.site.register(APIKey, APIKeyAdmin)