from django.contrib import admin
from .models import Dish, OrderInfo, OrderItem

admin.site.register(Dish)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['dish']


@admin.register(OrderInfo)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_of_customer', 'email', 'phone_number',
                    'pickup_time', 'comment', 'status']
    list_filter = ['pickup_time']
    inlines = [OrderItemInline]
