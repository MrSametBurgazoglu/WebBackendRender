from django.contrib import admin
from accounts.models import Customer


class CustomerAdmin(admin.ModelAdmin):

    list_display = ['name']

    class Meta:
        model = Customer


admin.site.register(Customer, CustomerAdmin)
