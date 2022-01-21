from django.contrib import admin
from .models import Autorizador


@admin.register(Autorizador)
class AutorizadorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'last_login', 'ativo']
