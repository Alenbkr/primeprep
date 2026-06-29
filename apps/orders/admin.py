from django.contrib import admin
from .models import DeliveryAddress, Order


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'apartment', 'is_default')
    list_filter = ('city',)
    search_fields = ('user__username', 'city', 'street')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ration', 'status', 'total_price', 'start_date', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
