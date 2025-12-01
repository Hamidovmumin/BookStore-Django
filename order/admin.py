from django.contrib import admin
from .models import Order,OrderItem,District,Division

@admin.register(Order)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user','name','email','phone','address','division','district','zip_code','payment_method','payable',)
    list_filter = ('user','email')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','book','price','quantity')
    list_filter  = ('order','book')

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name','division')
    list_filter = ('division',)