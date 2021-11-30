from django.db                  import models

# Create your models here.
class Package(models.Model):
    name           = models.CharField(max_length=100)
    description    = models.CharField(max_length=2000)
    price          = models.CharField(max_length=50)
    thumnail_image = models.CharField(max_length=2000)
    sales_volume   = models.IntegerField()
    category       = models.ForeignKey('Category',on_delete=models.CASCADE)
    product        = models.ManyToManyField('Product',related_name='packages')
    tag            = models.ManyToManyField('Tag',related_name='packages')
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

class Package_image(models.Model):
    image_url = models.CharField(max_length=2000)
    packages  = models.ForeignKey('Package')

    class Meta:
        db_table = 'package_images'

class Cart(models.Model):
    quantity  = models.IntegerField()
    package   = models.ForeignKey('Package',on_delete=models.CASCADE)
    user      = models.ForeignKey('User',on_delete=models.CASCADE)

    class Meta:
        db_table = 'carts'

class Order_item(models.Model):
    quantity   = models.IntegerField()
    package    = models.ForeignKey('Package',on_delete=models.CASCADE)
    order      = models.ForeignKey('Order',on_delete=models.CASCADE)
    user       = models.ForeignKey('User',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_items'

class Order(models.Model):
    order_number = models.CharField(max_length=100) # uuidField 
    status       = models.CharField(max_length=50)
    sub_total    = models.IntegerField()
    user         = models.ForeignKey('User',on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class User(models.Model):
    name     = models.CharField(max_length=50)
    address  = models.CharField(max_length=200)
    email    = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    class Meta:
        db_table = 'users'

class Tag(models.Model):
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'tags'

# class PackageTag(models.Model):
#     package = models.ForeignKey('Package',on_delete=models.CASCADE)
#     tags = models.ForeignKey('Tag',on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'package_tags'

# class PackageProduct(models.Model):
#     package = models.ManyToManyField('Package')
#     product = models.ManyToManyField('Product')

#     class Meta:
#         db_table = 'package_products'
