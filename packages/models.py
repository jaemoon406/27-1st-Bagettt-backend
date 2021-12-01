from django.db import models

class Package(models.Model):
    name           = models.CharField(max_length=100)
    description    = models.CharField(max_length=2000)
    price          = models.DecimalField(max_digits=9,decimal_places=2)
    thumnail_image = models.CharField(max_length=2000)
    sales_volume   = models.IntegerField(default=0)
    category       = models.ForeignKey('Category',on_delete=models.CASCADE)
    products       = models.ManyToManyField('Product',related_name='packages')
    tags           = models.ManyToManyField('Tag',related_name='packages')
    
    class Meta:
        db_table = 'packages'

class Product(models.Model):
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    brand_name  = models.CharField(max_length=200)
    image_url   = models.CharField(max_length=2000)
    kcal        = models.IntegerField()
    nutrition   = models.CharField(max_length=500)

    class Meta:
        db_table = 'products'

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

class PackageImage(models.Model):
    image_url = models.CharField(max_length=2000)
    packages  = models.ForeignKey('Package')

    class Meta:
        db_table = 'package_images'

class Cart(models.Model):
    quantity     = models.IntegerField()
    package      = models.ForeignKey('Package',on_delete=models.CASCADE)
    user         = models.ForeignKey('User',on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_add=True)

    class Meta:
        db_table = 'carts'

class OrderItem(models.Model):
    quantity   = models.IntegerField()
    package    = models.ForeignKey('Package',on_delete=models.CASCADE)
    order      = models.ForeignKey('Order',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_items'

class Order(models.Model):
    order_number = models.CharField(max_length=100)
    sub_total    = models.IntegerField()
    user         = models.ForeignKey('User',on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_add=True)

    class Meta:
        db_table = 'orders'

class User(models.Model):
    name     = models.CharField(max_length=50)
    address  = models.CharField(max_length=200)
    email    = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)

    class Meta:
        db_table = 'users'

class Tag(models.Model):
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'tags'

class Status(models.Model):
    oerder = models.ForeignKey('Order',on_delete=models.CASCADE)
    result = models.CharField(max_length=30)

    class Meta:
        db_table = 'statuses'