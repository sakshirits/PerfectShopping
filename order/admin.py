from django.contrib import admin
from .models import OrderItem,Order
# Register your models here.

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets =[
        ('Product' , {'fields':['product'],}),
        ('Quantity', {'fields': ['quantity'],}),
        ('Price', {'fields': ['price']}),

    ]
    readonly_fields = ['product','quantity','price']
    can_delete =False
    max_nm =0
    template = 'order/tabular.html'
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','billingName','emailAddress','created']
    list_display_links =['id','billingName']
    search_fields = ['id','billingName','emailAddress']
    readonly_fields = ['id','token','total','emailAddress','created','billingName','billingAddress','billingCity',
                       'billingPostcode','billingCountry','shippingName','shippingAddress','shippingCity','shippingPostcode',
                       'shippingCountry']
    fieldsets = [
        ('Order Information',{'fields':['id','token','total','created']}),
        (' Billing Information', {'fields': ['billingName','billingAddress','billingCity','billingPostcode','billingCountry','emailAddress']}),
        ('Shipping Information', {'fields': ['shippingName','shippingAddress','shippingCity','shippingPostcode', 'shippingCountry']})
    ]

    inlines = [
        OrderItemAdmin,
    ]
    def has_delete_permission(self,request,obj=None):
        return False

    def has_add_permission(self,request,obj=None):
        return False

