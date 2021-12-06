from os import PRIO_PROCESS
from django.db                      import models
from core.models                    import TimeStampModel

class Cart(TimeStampModel):
    quantity        = models.IntegerField()
    package         = models.ForeignKey('packages.Package',on_delete=models.CASCADE)
    user            = models.ForeignKey('users.User',on_delete=models.CASCADE)
    shipping_option = models.ForeignKey('Option',on_delete=models.CASCADE)
    price           = models.DecimalField(max_digits=9,decimal_places=2)

    class Meta:
        db_table = 'carts'

class Option(models.Model):
    shipping_option = models.IntegerField(null=True)

    class Meta:
        db_table = 'options'

class OrderItem(TimeStampModel):
    quantity   = models.IntegerField()
    package    = models.ForeignKey('packages.Package',on_delete=models.CASCADE)
    order      = models.ForeignKey('Order',on_delete=models.CASCADE)
 
    class Meta:
        db_table = 'order_items'

class Order(TimeStampModel):
    order_number    = models.CharField(max_length=100)
    sub_total       = models.DecimalField(max_digits=9,decimal_places=2)
    user            = models.ForeignKey('users.User',on_delete=models.CASCADE)
    shipping_option = models.ForeignKey('Option',on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

