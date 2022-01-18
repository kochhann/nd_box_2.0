from django.contrib import admin
from .models import ScheduledTask


@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    list_display = ['task', 'status', 'error_message', 'extra_field', 'ativo']
