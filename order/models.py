from django.db import models

# Create your models here.
class Order(models.Model):
    token = models.CharField(max_length=250)
    total = models.DecimalField(max_digits=10,decimal_places=2)
    emailAddress = models.EmailField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250)
    billingAddress = models.CharField(max_length=250)
    billingCity = models.CharField(max_length=250)
    billingPostcode = models.CharField(max_length=250)
    billingCountry = models.CharField(max_length=250)
    shippingName = models.CharField(max_length=250)
    shippingAddress = models.CharField(max_length=250)
    shippingCity = models.CharField(max_length=250)
    shippingPostcode = models.CharField(max_length=250)
    shippingCountry = models.CharField(max_length=250)

    class Meta:
        db_table = 'Order';
        ordering = ['-created']

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity =models.CharField(max_length=250)
    price = models.CharField(max_length=250)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


    class Meta:
        db_table = 'OrderItem'

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product


