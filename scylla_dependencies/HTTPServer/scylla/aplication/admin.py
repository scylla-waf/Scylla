from django.contrib import admin

from .models import Request


# Register your models here.

class AdminRequest(admin.ModelAdmin):
    list_display = ["ip", "petition"]
    list_editable = []


admin.site.register(Request, AdminRequest)
