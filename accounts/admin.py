from django.contrib import admin
from accounts.models import Customer
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):

    list_display = ['full_name']

    class Meta:
        model = Customer


admin.site.register(Customer, CustomerAdmin)
