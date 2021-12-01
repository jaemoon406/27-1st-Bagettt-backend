from django.db import models

class Cart(models.Model):
    quantity     = models.IntegerField()
    package      = models.ForeignKey('packages.Package',on_delete=models.CASCADE)
    user         = models.ForeignKey('users.User',on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

class OrderItem(models.Model):
    quantity   = models.IntegerField()
    package    = models.ForeignKey('packages.Package',on_delete=models.CASCADE)
    order      = models.ForeignKey('shops.Order',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_items'

class Order(models.Model):
    order_number = models.CharField(max_length=100)
    sub_total    = models.DecimalField(max_digits=9,decimal_places=2)
    user         = models.ForeignKey('users.User',on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
